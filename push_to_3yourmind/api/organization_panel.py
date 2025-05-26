"""
Groups API functionality from the User Panel, such as creating/updating baskets,
placing orders, making requests for quotes, ordering quotes etc.
"""

import datetime
import decimal
import typing as t
import time

from push_to_3yourmind import types, exceptions, utils
from push_to_3yourmind.logger import logger
from push_to_3yourmind.api.base import BaseAPI
from push_to_3yourmind.types import NoValue

__all__ = ["UserPanelAPI"]


class OrganizationPanelAPI(BaseAPI):
    """
    Accesseible via namespace `organization_panel`, for example:
    >>> response = client.organization_panel.get_baskets()
    """

    def get_users(
            self,
            *,
            page: t.Optional[int] = NoValue,
            page_size: t.Optional[int] = NoValue,
            search: t.Optional[str] = NoValue
    ) -> types.ResponseDict:
        """
        Get all users of the current organization. Returns paginated list.

        Args:
            page: int, optional
            page_size: int, optional
        Returns:
            dictionary with the following keys:

            - count: total number of baskets, int
            - currentPage: page number, int
            - totalPages: total number of pages, int
            - pageSize: baskets per page, int
            - results: list of basket details
        """
        query = self._get_parameters(page=page, pageSize=page_size, search=search)
        return self._request("GET", "organization-panel/users/", params=query)

    def get_user_preferences(self, *, user_id: int) -> types.ResponseDict:
        """
        Get region preferences for a User

        Args:
            user_id: id of user to get preferences from, int
        Returns:
            dictionary with the following keys:

            - language
            - currency
            - country
            - unit
        """
        return self._request("GET", f"organization-panel/users/{user_id}/preferences/")

    def get_user_addresses(self, *, user_id: int) -> types.ResponseDict:
        """
        Get addresses for a User

        Args:
            user_id: id of user to get addresses from, int
        Returns:
            list with all addresses from user.
        """
        return self._request("GET", f"organization-panel/users/{user_id}/addresses/")

    def create_user(
            self,
            *,
            email: str,
            first_name: str,
            last_name: str,
            is_active: t.Optional[bool] = True,
    ) -> types.ResponseDict:
        """
        Create a new user

        Args:
            email: email address of the user,
            first_name: user's first name,
            last_name: user's last name,
            is_active: user should be verified automatically
        Returns:
            full user profile.
        """
        return self._request(
            "POST",
            f"organization-panel/users/create/",
            json={
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "isActive": is_active,
            },
        )

    def update_user_preferences(
            self,
            *,
            user_id: int,
            country: types.OptionalString = types.NoValue,
            currency: types.OptionalString = types.NoValue,
            language: types.OptionalString = types.NoValue,
            unit: types.OptionalString = types.NoValue,
    ) -> types.ResponseDict:
        """
        Update profile of the user matching the provided id. All other arguments are
        optional, only passed values will be saved to the profile.

        Args:
            user_id: id of the user whos preferences shauld be updated
            country: 2-letter country code, ex. US, FR, GB
            currency: 3-letter currency code, ex. USD, EUR
            language: 2-letter language code, ex. en, de, fr, es
            unit: mm or inch
        """

        json = self._get_parameters(
            country=country, currency=currency, language=language, unit=unit
        )
        return self._request(
            "PUT",
            f"organization-panel/users/{user_id}/preferences/",
            json=json
        )

    def create_user_address(
            self,
            *,
            city: str,
            country: str,
            first_name: str,
            last_name: str,
            line1: str,
            phone_number: str,
            user_id: str,
            zip_code: str,
            company_name: str = types.NoValue,
            department: str = types.NoValue,
            line2: str = types.NoValue,
            state: str = types.NoValue,
            title: str = types.NoValue,
            vat_id: str = types.NoValue,
    ) -> types.ResponseDict:
        """
        Create a new address for a user. If it is the first address that is created for the
        user, it will become their default address automatically
        """

        json = self._get_parameters(
            city=city,
            country=country,
            companyName=company_name,
            department=department,
            firstName=first_name,
            lastName=last_name,
            line1=line1,
            line2=line2,
            phoneNumber=phone_number,
            state=state,
            title=title,
            vatId=vat_id,
            zipCode=zip_code
        )
        return self._request(
            "POST",
            f"organization-panel/users/{user_id}/addresses/",
            json=json
        )


