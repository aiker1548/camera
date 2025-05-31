# from collections import OrderedDict
# from typing import Optional, Dict

# import vertica_python
# from vertica_python.vertica.cursor import Cursor


# class Vertica:
#     def __init__(self, config: Dict):
#         self.config = config

#     def _fetch_one(self, query: str, params: dict = None) -> Optional[OrderedDict]:
#         params = params or {}
#         with vertica_python.connect(**self.config) as connect:
#             cursor: Cursor = connect.cursor("dict")
#             cursor.execute(query, params)
#             return cursor.fetchone() or []

#     def _fetch_many(self, query: str, params: dict = None) -> list:
#         params = params or {}
#         with vertica_python.connect(**self.config) as connect:
#             cursor: Cursor = connect.cursor("dict")
#             cursor.execute(query, params)
#             return cursor.fetchall() or []
