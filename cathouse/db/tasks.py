import logging
from fastapi import FastAPI
from databases import Database

from cathouse.api.dependencies.settings import get_settings


logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    settings = get_settings()

    if settings.database_url.scheme == "postgresql":
        database = Database(
            settings.database_url, min_size=2, max_size=10,
        )
    else:
        database = Database(settings.database_url)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")


