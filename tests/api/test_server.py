import logging
import os
import pytest
from httpx import AsyncClient
from databases import Database
from devtools import debug

from cathouse.api import server
from cathouse.api.dependencies.database import get_database

logger = logging.getLogger(__name__)


def get_test_postgres_url():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    server = os.getenv("POSTGRES_SERVER")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"


async def override_get_database():
    database = Database(get_test_postgres_url(), min_size=2, max_size=10)
    try:
        await database.connect()
        return database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


app = server.get_application()
app.dependency_overrides[get_database] = override_get_database

test_cat = {
    "name": "Merlin",
    "age": 2,
    "kind": "Russian Blue",
    "sex": "MALE",
    "favorite_foods": [
        "Ice Cream",
        "Blue's Food"
    ],
    "owner": "Emma and Andrew"
}


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/cat", json=test_cat)
        debug(response)
        assert response.status_code == 201
        assert isinstance(response.json()["id"], int)
        response_json = response.json()
        assert response_json == {
            "id": 1,
            "name": "Merlin",
            "age": 2,
            "kind": "Russian Blue",
            "sex": "MALE",
            "favorite_foods": [
                "Ice Cream",
                "Blue's Food"
            ],
            "owner": "Emma and Andrew"
        }
