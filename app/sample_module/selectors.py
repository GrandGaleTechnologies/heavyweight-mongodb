"""This module contains the selectors i.e. the functions that return something from the db for the example module."""

from typing import cast

from pydantic import UUID4

from app.sample_module import db
from app.sample_module.exceptions import UserNotFound
from app.sample_module.schemas import UserDocument


async def get_user_by_id(id: UUID4, raise_exc: bool = True):
    """
    Get user by ID

    Args:
        id (UUID4): The user's ID
        raise_exc (bool, optional): raise a 404 if not found. Defaults to True.

    Raises:
        UserNotFound

    Returns:
        UserDocumentType: The user document
    """
    # Get collection
    user_col = db.get_user_collection()

    # Get obj
    user = cast(UserDocument | None, await user_col.find_one({"id": str(id)}))

    if not user and raise_exc:
        raise UserNotFound()

    return user
