from functools import lru_cache

from pymongo import AsyncMongoClient

from app.core.settings import get_settings

# Globals
settings = get_settings()


# Constants.
DBNAME = "main"
# NOTE: key = name of the collection, items = indexes
COLLECTIONS = {"test": ["id"]}


@lru_cache()
def get_client():
    """
    Get mongodb client
    """
    return AsyncMongoClient(
        settings.MONGODB_URL,
        tz_aware=True,
        uuidRepresentation="standard",
    )


async def setup_mongodb():
    """
    Setup MongoDB database and collections
    """
    # Get client
    client = get_client()

    # Check if DB exists (Mongo creates DBs/collections lazily)
    existing_dbs = await client.list_database_names()
    if DBNAME not in existing_dbs:
        # Trigger DB creation with dummy insert
        dummy_db = client["main"]
        await dummy_db["__init__"].insert_one({"_init": True})
        await dummy_db["__init__"].drop()

    db = client[DBNAME]

    # Check if collection exists
    existing_collections = await db.list_collection_names()
    for collection, indexes in COLLECTIONS.items():
        if collection not in existing_collections:
            col = await db.create_collection(collection)

            for index in indexes:
                await col.create_index(index)

    return db
