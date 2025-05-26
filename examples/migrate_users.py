import logging
import json
import sys

import push_to_3yourmind as pt3

logger = logging.getLogger(__name__)

stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)

logger.addHandler(stdout)
logger.setLevel(logging.INFO)


class GatherUsersException(Exception):
    pass


class CreateUserException(Exception):
    pass


class EmailAlreadyExistsException(Exception):
    pass


class TransferPreferencesException(Exception):
    pass


class TransferAddressesException(Exception):
    pass


class UserMigrator:
    def __init__(
            self,
            origin_access_token: str,
            origin_base_url: str,
            target_access_token: str,
            target_base_url: str,
    ):
        self.origin_client = pt3.PushTo3YourmindAPI(
            access_token=origin_access_token,
            base_url=origin_base_url
        )
        self.target_client = pt3.PushTo3YourmindAPI(
            access_token=target_access_token,
            base_url=target_base_url,
        )

    def gather_users(self) -> tuple[list[pt3.td.ResponseDict], int]:
        users = []
        page = 1
        while True:
            try:
                users_from_page = self.origin_client.organization_panel.get_users(page=page, page_size=100)
            except pt3.BasePushTo3YourmindAPIException as e:
                logger.info(f"Error while gathering users on page {page}: {e}")
                raise GatherUsersException(e)
            else:
                users.extend(users_from_page["results"])
                logger.info(f"Gathering users: {len(users)}/{users_from_page['count']}")

                if len(users) == users_from_page['count']:
                # if len(users) >= 10:
                    return users, users_from_page["count"]
            finally:
                page += 1

    def transfer_user(self, user: pt3.td.ResponseDict):
        old_user_id = user["id"]
        old_user_default_address_id = user["defaultAddressId"]
        user_already_exists = False
        # Create user in target platform
        try:
            new_user = self.target_client.organization_panel.create_user(
                email=user["email"],
                first_name=user["firstName"],
                last_name=user["lastName"],
            )
        except pt3.BasePushTo3YourmindAPIException as e:
            if "A user with this email address already exits" in str(e):
                logger.info(f"User with the email of User<id={old_user_id}> already exists, skip")
                raise EmailAlreadyExistsException(e)

            logger.info(f"Failed to create user from User<id={old_user_id}> in origin platform")
            raise CreateUserException(e)

        # Sync Preferences
        try:
            response = self.origin_client.organization_panel.get_user_preferences(
                user_id=old_user_id
            )
            if response["country"] is None:
                response["country"] = "US"
            self.target_client.organization_panel.update_user_preferences(
                user_id=new_user["id"],
                **response
            )
        except pt3.BasePushTo3YourmindAPIException as e:
            logger.info(f"Failed to transfer from User<id={user['id']}> in origin platform")
            raise TransferPreferencesException(e)

        # Sync Addresses
        if user_already_exists:
            try:
                target_addresses = self.target_client.organization_panel.get_user_addresses(
                    user_id=new_user["id"]
                )
                if target_addresses:
                    logger.info("User in target platform already has addresses. "
                                "Skipping Address sync.")
                    return new_user
            except pt3.BasePushTo3YourmindAPIException:
                pass

        try:
            addresses = self.origin_client.organization_panel.get_user_addresses(
                user_id=old_user_id
            )
        except pt3.BasePushTo3YourmindAPIException as e:
            raise TransferAddressesException(e)

        if old_user_default_address_id:
            addresses = sorted(
                addresses,
                key=lambda addr: abs(addr["id"] - old_user_default_address_id)
            )

        failed_addresses = []
        for address in addresses:
            try:
                self.target_client.organization_panel.create_user_address(
                    user_id=new_user["id"],
                    city=address["city"],
                    country=address["country"],
                    first_name=address["firstName"],
                    last_name=address["lastName"],
                    line1=address["line1"],
                    phone_number=address["phoneNumber"],
                    zip_code=address["zipCode"],
                    company_name=address["companyName"],
                    department=address["department"],
                    line2=address["line2"],
                    state=address["state"],
                    title=address["title"],
                    vat_id=address["vatId"],
                )
            except pt3.BasePushTo3YourmindAPIException as e:
                failed_addresses.append((address["id"], e))

        if failed_addresses:
            failed_addresses = ", ".join(str(f) for f in failed_addresses)
            raise TransferAddressesException(
                f"Transfer of addresses failed for addresses with ids {failed_addresses}"
            )

    def test_connections(self):
        try:
            response = self.origin_client.organization_panel.get_users(page=1, page_size=25)
            logger.info("Connection to origin is established")
            logger.info(f"Origin platform has {response['count']} users")

            response = self.target_client.organization_panel.get_users(page=1, page_size=25)
            logger.info("Connection to target is established")
            logger.info(f"Target platform has {response['count']} users")
        except pt3.BasePushTo3YourmindAPIException as e:
            raise Exception("Connection could not be established")

    def migrate(self):
        users, user_count = self.gather_users()
        logger.info(f"Starting to migrate {user_count} users.")
        if len(users) != user_count:
            logger.warning(
                f"Number of gathered users ({len(users)}) does not match "
                f"the number of users given by the platform *{user_count}"
            )

        record = []
        for user in users:
            try:
                self.transfer_user(user)
            except CreateUserException as e:
                logger.warning(f"User(id={user['id']}): Failed to create user: {str(e)[:256]}")
                record.append({"user_id": user["id"], "error": "create_user", "error_reason": str(e)})
            except EmailAlreadyExistsException as e:
                record.append({"user_id": user["id"], "error": None, "error_reason": "Email already exists"})
            except TransferPreferencesException as e:
                logger.warning(f"User(id={user['id']}): Failed to transfer preferences: {str(e)[:256]}")
                record.append({"user_id": user["id"], "error": "transfer_preferences", "error_reason": str(e)})
            except TransferAddressesException as e:
                logger.warning(f"User(id={user['id']}): Failed to transfer addresses: : {str(e)[:256]}")
                record.append({"user_id": user["id"], "error": "transfer_addresses", "error_reason": str(e)})
            else:
                logger.info(f"User(id={user['id']}): Succeeded")
                record.append({"user_id": user["id"], "error": None})


        logger.info(json.dumps(record))

        with open("log.json", "w") as f:
            json.dump(record, f, indent=2)

        logger.info("-- " * 20)
        logger.info("Migration has run")
        total_transfers = len(record)
        successful_transfers = sum(r["error"] is None for r in record)
        failed_transfers = total_transfers - successful_transfers
        logger.info(f"Total transfers: {total_transfers}")
        logger.info(f"Successful transfers: {successful_transfers}")
        logger.info(f"failed transfers: {failed_transfers}")

        if failed_transfers > 0:
            failed_user_creations = sum(r["error"] == "create_user" for r in record)
            failed_preference_transfers = sum(r["error"] == "transfer_preferences" for r in record)
            failed_address_transfers = sum(r["error"] == "transfer_addresses" for r in record)
            logger.info(f"\tfailed user creations: {failed_user_creations}")
            logger.info(f"\tfailed preference transfors: {failed_preference_transfers}")
            logger.info(f"\tfailed address transfers: {failed_address_transfers}")


if __name__ == "__main__":
    logger.info("Let's go!")
    migrator = UserMigrator(
        origin_base_url="https://protocam.prototek.com",
        origin_access_token="a34b8e64ea9e646eb5adf7afeccb78a91cb6c265",
        target_base_url="https://instantquote.prototek.com",
        target_access_token="f49e89458b813992d69a9a3b511813e5534dd037"
    )
    # migrator = UserMigrator(
    #     origin_base_url="https://protocam.prototek.com",
    #     origin_access_token="a34b8e64ea9e646eb5adf7afeccb78a91cb6c265",
    #     target_base_url="http://multi.my.3yd",
    #     target_access_token="8a1ff31f6ca5fed599242ac520fe67eda5bcd30f"
    # )
    migrator.migrate()
