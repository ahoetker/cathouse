from fastapi import APIRouter
from cathouse.api.routes.cats import (
    router as cats_router,
)

router = APIRouter()
router.include_router(cats_router, prefix="/cat", tags=["cats"])
