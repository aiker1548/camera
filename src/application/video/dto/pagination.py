from typing import Optional

class PaginationParams:
    offset: int
    limit: int
    sort_by: Optional[str]   
    sort_desc: bool

    def __init__(
        self,
        offset: int = 0,
        limit: int = 10,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
    ):
        self.offset = offset
        self.limit = limit
        self.sort_by = sort_by
        self.sort_desc = sort_desc

    @classmethod
    def from_dict(cls, data: dict) -> "PaginationParams":
        return cls(
            offset=data.get("offset", 0),
            limit=data.get("limit", 10),
            sort_by=data.get("sort_by"),
            sort_desc=data.get("sort_desc", False),
        )
    def to_dict(self) -> dict:
        return {
            "offset": self.offset,
            "limit": self.limit,
            "sort_by": self.sort_by,
            "sort_desc": self.sort_desc,
        }
