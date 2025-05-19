import csv
from dataclasses import dataclass
import io
import logging
import typing as t

import push_to_3yourmind

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


"""
An example script that uses push_to_3yourmind to read out a csv
and import the data to catalog items in an example platform.

However, with providing real world config data and a custom
mapper function this script can be used in a production environment
as well.
"""

@dataclass
class ItemData:
    cad_file: str
    product_id: int
    post_processings: push_to_3yourmind.td.PostProcessingConfig
    part_requirements: t.Optional[push_to_3yourmind.td.FormData]
    attachments: t.Optional[t.Sequence[str]]


class MapperException(Exception):
    """
    Should be raised by a mapper function if necessary
    """
    pass


MapperFunction = t.Callable[[dict], ItemData]


class ImportCatalogClient:
    """
    Wraps an Api client instance and offers helper functions for a simple
    workflow creating multiple catalog items.
    """
    def __init__(self, access_token: str, base_url: str):
        self.client = push_to_3yourmind.PushTo3YourmindAPI(
            access_token=access_token,
            base_url=base_url,
        )
        
    def list_form_details(self):
        return self.client.common.get_forms()
        
    def create_basket(self):
        return self.client.user_panel.create_basket()

    def create_basket_item(
            self,
            *,
            basket_id: int,
            file: t.Union[str, io.BytesIO],
            product_id: int,
            post_processings: t.List[push_to_3yourmind.td.PostProcessingConfig] = (),
            part_requirements: t.Optional[push_to_3yourmind.td.FormData] = None,
    ):
        line = self.client.user_panel.create_line_with_cad_file_and_product(
            basket_id=basket_id,
            cad_file=file,
            quantity=1,
            product_id=product_id,
            # post_processings=post_processings,
        )
        if part_requirements is not None:
            self.client.user_panel.add_part_requirements_to_basket_line(
                line_id=line["id"],
                form_data=part_requirements,
            )
        return line
    
    def create_catalog_item(self, *, basket_line_id: int):
        return self.client.user_panel.create_catalog_item(
            basket_line_id=basket_line_id,
        )

    def add_attachments_to_catalog_item(
            self,
            catalog_item_id: int,
            attachment: t.Union[str, io.BytesIO],
    ):
        self.client.user_panel.upload_catalog_item_attachment(
            catalog_item_id=catalog_item_id,
            attachment_file=attachment,
        )

    def delete_basket(self, basket_id: int):
        # Clean up helper basket
        self.client.user_panel.delete_basket(basket_id=basket_id)


api_client = ImportCatalogClient(
    access_token="",
    base_url="",
)
        

def import_catalog_items(csv_path: str, mapper: MapperFunction, is_dry_run=True) -> None:
    """
    Will do all transformations and api calls to turn

    :param conf: Contains base config for this process
    :param mapper: function that will transform a line in a csv file
                   and turns it into an ItemData struct
    """
    basket = api_client.create_basket()

    logger.info("Start to read csv files")
    with open(csv_path) as f:
        csv_reader = csv.DictReader(f)

        for index, line in enumerate(csv_reader):
            logger.info(f"Reading line {index} of csv file")
            try:
                item_data = mapper(line)
            except MapperException as e:
                logger.error(f"Mapping Failed: {e}")
                continue

            try:
                basket_line = api_client.create_basket_item(
                    basket_id=basket["id"],
                    file=item_data.cad_file,
                    product_id=item_data.product_id,
                    # part_requirements=item_data.part_requirements,
                    # post_processings=item_data.post_processings,
                )
            except push_to_3yourmind.BasePushTo3YourmindAPIException as e:
                logger.error(f"One Api call failed: {e}")
                continue
                
            if not is_dry_run:
                catalog_item = api_client.create_catalog_item(
                    basket_line_id=basket_line["id"],
                )
                    
                for attachment in item_data.attachments:
                    print("attachment:", attachment)
                    api_client.add_attachments_to_catalog_item(
                        catalog_item_id=catalog_item["id"],
                        attachment=attachment,
                    )

    api_client.delete_basket(basket_id=basket["id"])


if __name__ == "__main__":
    import os
    import pathlib

    CSV_PATH = "./example.csv"

    # Get path to folder with example files
    BASE_DIR = pathlib.Path(os.getcwd())
    DATA_DIR = BASE_DIR / 'data'

    # function_map = {
    #     "aerospace": 4,
    #     "automotive": 5,
    # }
    
    # def create_form(function: t.Literal["aerospace", "automotive"]):
    #     try:
    #         function_id = function_map[function]
    #     except KeyError:
    #         raise MapperException("Unknown function")
        
    #     return push_to_3yourmind.td.FormData(
    #         form_id=1,
    #         fields=[
    #             push_to_3yourmind.td.FormField(
    #                 form_field_id=3,
    #                 value=function_id
    #             )
    #         ]
    #     )

    def mapper_func(data: dict) -> ItemData:
        """
        Takes one dict (parsed from a csv file in this example, but can
        come from anywhere) and turns it into data that is understandable
        by the client
        """
        # if post_processing_ids := data["post_processing_ids"]:
        #     post_processings = [
        #         push_to_3yourmind.td.PostProcessingConfig(
        #             post_processing_id=int(entry),
        #             color_id=None,
        #         )
        #         for entry in post_processing_ids.split(" ")
        #     ]
        # else:
        post_processings = []

        # create part requirements from data
        # part_requirements = create_form(data["function"])

        cad_file_path = str(DATA_DIR / data["stl_file"])
        attachments = [str(DATA_DIR / file_name) for file_name in data["attachments"].split(" ") if file_name]
        return ItemData(
            cad_file=cad_file_path,
            product_id=data["productId"],
            part_requirements=None,
            post_processings=post_processings,
            attachments=attachments,
        )

    import_catalog_items(CSV_PATH, mapper_func, is_dry_run=False)
