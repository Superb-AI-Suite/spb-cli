# from io import BytesIO
# from zipfile import ZipFile
# from urllib.request import urlopen
# from copy import deepcopy
# import simplejson as json


# def get_url_data(url: str) -> bytes:
#     return urlopen(url).read()


# def parse_zip_file(data: bytes) -> dict:
#     parsed_file = dict()
#     with ZipFile(BytesIO(data)) as zip_file:
#         file_names = zip_file.namelist()
#         for file_name in file_names:
#             parsed_file[file_name] = json.loads(zip_file.open(file_name, "r").read())
#     return (len(file_names), parsed_file)