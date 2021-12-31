from pydantic import BaseModel, PositiveInt
from enum import Enum
from typing import Optional
from app.const import FILENAME


class SortEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class QueryModel(BaseModel):
    filter: Optional[str]
    limit: Optional[PositiveInt]
    sort: Optional[SortEnum]
    map: Optional[PositiveInt]
    unique: Optional[bool]
    filename: str = FILENAME

    class Config:
        orm_mode = True


class CmdEnum(str, Enum):
    filter = "filter"
    limit = "limit"
    map = "map"
    sort = "sort"
    unique = "unique"


class BodyModel(BaseModel):
    filename: str = FILENAME
    cmd1: CmdEnum
    value1: str
    cmd2: CmdEnum
    value2: str

    class Config:
        orm_mode = True
