from time import localtime
from push_to_3yourmind.exceptions import FileAnalysisError
import csv
from dataclasses import dataclass
import io
import logging
import typing as t

import push_to_3yourmind
from venv import create
from push_to_3yourmind.api import user_panel

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
    detailed_description: t.Optional[str]
    partner_id: t.Optional[int]
    post_processing_product_ids: list[int]
    product_id: int
    reference: t.Optional[str]
    short_description: t.Optional[str]
    status: t.Literal['published', 'unpublished']
    stl_file_uuid: str
    technology_id: int
    title: str
    attachments: list[str]


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

    def create_catalog_item(self, item: ItemData):
    	return self.client.user_panel.create_catalog_item(
	        detailed_description=item.detailed_description,
	        partner_id=item.partner_id,
	        post_processing_product_ids=item.post_processing_product_ids,
	        product_id=item.product_id,
	        reference=item.reference,
	        short_description=item.short_description,
	        status=item.status,
	        stl_file_uuid=item.stl_file_uuid,
	        technology_id=item.technology_id,
	        title=item.title,
    	)

    def add_attachments_to_catalog_item(
            self,
            catalog_item_id: int,
            attachment: t.Union[str, io.BytesIO],
    ):
        return self.client.user_panel.upload_catalog_item_attachment(
            catalog_item_id=catalog_item_id,
            attachment_file=attachment,
        )


api_client = ImportCatalogClient(
    access_token="7a625662655dd88c6e0d3bf8fe21ecf3b6ab5b77",
    base_url="https://24-12-x.stage.3yourmind-internal.com",
)


def import_catalog_items(csv_path: str, mapper: MapperFunction, is_dry_run=True) -> None:
    """
    Will do all transformations and api calls to turn

    :param conf: Contains base config for this process
    :param mapper: function that will transform a line in a csv file
                   and turns it into an ItemData struct
    """
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

            catalog_item = api_client.create_catalog_item(
               	item_data,
            )

            for attachment in item_data.attachments:
                print("attachment:", attachment)
                api_client.add_attachments_to_catalog_item(
                    catalog_item_id=catalog_item["id"],
                    attachment=attachment,
                )


if __name__ == "__main__":
    import os
    import pathlib
    import time

    CSV_PATH = "./example.csv"

    # Get path to folder with example files
    BASE_DIR = pathlib.Path(os.getcwd())
    DATA_DIR = BASE_DIR / 'data'

    def mapper_func(data: dict) -> ItemData:
        """
        Takes one dict (parsed from a csv file in this example, but can
        come from anywhere) and turns it into data that is understandable
        by the client
        """

        cad_file_path = str(DATA_DIR / data["stl_file"])
        attachments = [str(DATA_DIR / file_name) for file_name in data["attachments"].split(" ") if file_name]

        upload = api_client.client.user_panel.upload_cad_file(
        	cad_file=cad_file_path,
        	unit="mm",
        )

        try:
        	api_client.client.user_panel.wait_for_analysis(file_uuid=upload["uuid"])
        except push_to_3yourmind.FileAnalysisError:
        	raise MapperException("File anlysis failed or took too long")

        return ItemData(
	        detailed_description=None,
			partner_id=int(data["partnerId"]),
			post_processing_product_ids=[],
			product_id=int(data["productId"]),
			reference=data["reference"],
			short_description=data["shortDescription"],
			status="published",
			stl_file_uuid=upload["uuid"],
			technology_id=int(data["technologyId"]),
			title=data["title"],
			attachments=attachments,
        )

    import_catalog_items(CSV_PATH, mapper_func, is_dry_run=False)
