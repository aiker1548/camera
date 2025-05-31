# """
# Sync Vertica client.
# """

# from collections import OrderedDict
# from typing import Optional

# from .base import Vertica


# class SyncVertica(Vertica):
#     def fetch_one(self, query: str, params: dict = None) -> Optional[OrderedDict]:
#         return self._fetch_one(query, params)

#     def fetch_many(self, query: str, params: dict = None) -> list:
#         return self._fetch_many(query, params)
