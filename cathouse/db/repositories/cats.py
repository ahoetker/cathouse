from cathouse.db.repositories.base import BaseRepository
from cathouse.models.cat import CatInDB, CatCreate, CatUpdate

from pydantic import parse_obj_as

from typing import List


CREATE_CAT_QUERY = """
    INSERT INTO cats (name, kind, age, sex, favorite_foods, owner)
    VALUES (:name, :kind, :age, :sex, :favorite_foods, :owner)
    RETURNING *;
"""

READ_CAT_QUERY = """
    SELECT id, name, kind, age, sex, favorite_foods, owner FROM cats
    WHERE id = :id;
"""

READ_CATS_QUERY = """
    SELECT id, name, kind, age, sex, favorite_foods, owner FROM cats;
"""

UPDATE_CAT_QUERY = """
    UPDATE cats
    SET 
        name = :name, 
        kind = :kind, 
        age = :age, 
        sex = :sex, 
        favorite_foods = :favorite_foods,
        owner = :owner
    WHERE id = :id
    RETURNING *;
"""

DELETE_CAT_QUERY = """
    DELETE FROM cats
    WHERE id = :id
    RETURNING *;
"""


class CatsRepository(BaseRepository):
    """ "
    All database actions associated with the User resource
    """

    # Create
    async def create_cat(self, *, new_cat: CatCreate) -> CatInDB:
        cat = await self.db.fetch_one(query=CREATE_CAT_QUERY, values=new_cat.dict())
        return CatInDB(**cat)

    # Read
    async def get_cat(self, *, id: int) -> CatInDB:
        cat = await self.db.fetch_one(query=READ_CAT_QUERY, values={"id": id})
        return CatInDB(**cat)

    async def get_cats(self) -> List[CatInDB]:
        cats = await self.db.fetch_all(query=READ_CATS_QUERY)
        return parse_obj_as(List[CatInDB], cats)

    # Update
    async def update_cat(self, *, id: int, cat_update: CatUpdate) -> CatInDB:
        query_values = cat_update.dict()
        query_values["id"] = id
        cat = await self.db.fetch_one(query=UPDATE_CAT_QUERY, values=query_values)
        return CatInDB(**cat)

    # Delete
    async def delete_cat(self, *, id: int) -> CatInDB:
        cat = await self.db.fetch_one(query=DELETE_CAT_QUERY, values={"id": id})
        return CatInDB(**cat)


