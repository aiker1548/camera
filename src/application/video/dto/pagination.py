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
