from fastapi import APIRouter
from cathouse.api.routes.cats import (
    router as cats_router,
)
from cathouse.api.routes.frontend import (
    router as frontend_router,
)

router = APIRouter()
router.include_router(cats_router, prefix="/cat", tags=["cats"])
# router.include_router(frontend_router, prefix="", tags=["frontend"])
