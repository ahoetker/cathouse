from pydantic.types import conint
from typing import List
from enum import Enum
from cathouse.models.core import CoreModel, IDModelMixin


class Sex(str, Enum):
    male = "MALE"
    female = "FEMALE"


class CatBase(CoreModel):
    name: str
    kind: str
    age: conint(ge=0)
    sex: Sex
    favorite_foods: List[str]
    owner: str


class CatCreate(CatBase):
    pass


class CatUpdate(CatBase):
    pass


class CatInDB(CatBase, IDModelMixin):
    pass


class CatPublic(CatInDB):
    pass


