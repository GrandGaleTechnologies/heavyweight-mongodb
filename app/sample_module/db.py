from functools import lru_cache

from app.core.database import get_client


@lru_cache()
# NOTE: lru_cache with async objects is still a vague line for us, requires more research
def get_user_collection():
    """
    Get users collection
    """
    mongodb_client = get_client()

    return mongodb_client["main"].get_collection("test")
