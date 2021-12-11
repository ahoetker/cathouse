from cathouse.api.dependencies.database import get_repository
from cathouse.db.repositories.cats import CatsRepository
from cathouse.models.cat import CatCreate, CatPublic, CatUpdate

from fastapi import APIRouter, Depends

from typing import List


router = APIRouter()


@router.post("/", response_model=CatPublic, status_code=201)
async def create_cat(
        cat: CatCreate,
        cats_repo: CatsRepository = Depends(get_repository(CatsRepository)),
) -> CatPublic:
    created_cat = await cats_repo.create_cat(new_cat=cat)
    return CatPublic(**created_cat.dict())


@router.get("/{id}", response_model=CatPublic)
async def read_cat(
        id: int,
        cats_repo: CatsRepository = Depends(get_repository(CatsRepository)),
) -> CatPublic:
    created_cat = await cats_repo.get_cat(id=id)
    return CatPublic(**created_cat.dict())


@router.get("/", response_model=List[CatPublic])
async def read_all_cats(
        cats_repo: CatsRepository = Depends(get_repository(CatsRepository)),
) -> List[CatPublic]:
    cats = await cats_repo.get_cats()
    return [CatPublic(**cat.dict()) for cat in cats]


@router.put("/{id}", response_model=CatPublic)
async def update_cat(
        id: int,
        cat: CatUpdate,
        cats_repo: CatsRepository = Depends(get_repository(CatsRepository)),
) -> CatPublic:
    updated_cat = await cats_repo.update_cat(id=id, cat_update=cat)
    return CatPublic(**updated_cat.dict())


@router.delete("/{id}", response_model=CatPublic)
async def delete_cat(
        id: int,
        cats_repo: CatsRepository = Depends(get_repository(CatsRepository)),
) -> CatPublic:
    deleted_cat = await cats_repo.delete_cat(id=id)
    return CatPublic(**deleted_cat.dict())


