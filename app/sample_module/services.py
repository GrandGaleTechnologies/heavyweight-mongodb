"""This module contains the services i.e. the functions that interact with the db for the example module."""

import uuid

from fastapi.encoders import jsonable_encoder

from app.sample_module import db, schemas


async def create_user(data: schemas.UserCreate):
    """
    Create user entry in db

    Args:
        data (schemas.UserCreate): The user's details

    Returns:
        schemas.User: The user obj
    """
    # Get collection
    user_collection = db.get_user_collection()

    # Form data
    user_data = schemas.User(id=uuid.uuid4(), **data.model_dump())

    # Save user
    await user_collection.insert_one(jsonable_encoder(user_data))

    return user_data
