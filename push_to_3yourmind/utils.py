from io import IOBase, BytesIO

import requests

from push_to_3yourmind import types, exceptions


def extract_file_content(file: types.CadFileSpecifier) -> BytesIO:
    if isinstance(file, str):
        if file.startswith("http"):
            response = requests.get(file)
            if response.status_code != 200:
                raise exceptions.CADFileNotFoundError(response.content)
            extracted_file_contents = BytesIO(response.content)
            extracted_file_contents.name = "originalFile.stl"
        else:
            try:
                with open(file, "rb") as cad_file_obj:
                    extracted_file_contents = BytesIO(cad_file_obj.read())
                    extracted_file_contents.name = cad_file_obj.name
            except IOError as exc:
                raise exceptions.CADFileNotFoundError from exc

    elif isinstance(file, IOBase):
        extracted_file_contents = file

    else:
        raise exceptions.BadArgument(
            "cad_file argument must be either a path to the CAD file "
            "or a file-like object"
        )

    return extracted_file_contents
