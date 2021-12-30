from pydantic import BaseModel, PositiveInt
from enum import Enum
from typing import Optional


class SortEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class QueryModel(BaseModel):
    filter: Optional[str]
    limit: Optional[PositiveInt]
    sort: Optional[SortEnum]
    map: Optional[PositiveInt]
    unique: Optional[bool]
    filename: str = "apache_logs.txt"

    class Config:
        orm_mode = True


class CmdEnum(str, Enum):
    filter = "filter"
    limit = "limit"
    map = "map"
    sort = "sort"
    unique = "unique"


class BodyModel(BaseModel):
    filename: str = "apache_logs.txt"
    cmd1: CmdEnum
    value1: str
    cmd2: CmdEnum
    value2: str

    class Config:
        orm_mode = True
