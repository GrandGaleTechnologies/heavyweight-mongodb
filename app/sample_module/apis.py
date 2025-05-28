"""This module contains the API endpoints for the example module."""

from typing import cast

from fastapi import APIRouter
from pydantic import UUID4
from pymongo import ASCENDING, DESCENDING

from app.common.annotations import PaginationParams
from app.common.paginators import get_pagination_metadata_mongo
from app.common.schemas import ResponseSchema
from app.sample_module import db, schemas, selectors, services

router = APIRouter()


NAMES = [
    {
        "first_name": "Alice",
        "last_name": "Wonderland",
    },
    {
        "first_name": "Bob",
        "last_name": "Builder",
    },
    {
        "first_name": "Charlie",
        "last_name": "Chaplin",
    },
    {
        "first_name": "Dora",
        "last_name": "Explorer",
    },
]


@router.post(
    "",
    summary="Create user in db",
    response_description="The details of the created user",
    status_code=201,
    response_model=schemas.UserResponse,
)
async def route_users_create(user_in: schemas.UserCreate):
    """
    This endpoint is used to create a new user entry
    """

    # Create user
    user = await services.create_user(data=user_in)

    return {"data": user}


@router.get(
    "/{user_id}/",
    summary="Get user details",
    response_description="The details of the user",
    status_code=200,
    response_model=schemas.UserResponse,
)
async def route_user_details(user_id: UUID4):
    """
    This is an example endpoint
    """

    # Get user
    user = await selectors.get_user_by_id(id=user_id)

    return {"data": user}


@router.get(
    "",
    summary="Get user list",
    response_description="The paginated list of users",
    status_code=200,
    response_model=schemas.PaginatedUserListResponse,
)
async def route_user_list(pag: PaginationParams):
    """
    This endpoint returns the paginated list of users
    """

    # Get collection
    user_col = db.get_user_collection()

    # Filter setup
    filters = {}

    if pag.q:
        filters["$and"] = []
        filters["$and"].append(
            {
                "$or": [
                    {"first_name": {"$regex": pag.q, "$options": "i"}},
                    {"last_name": {"$regex": pag.q, "$options": "i"}},
                ]
            }
        )

    # Sorting
    order_by = ASCENDING if pag.order_by == "asc" else DESCENDING

    # Query
    results = (
        user_col.find(filters if filters else None)
        .sort("first_name", order_by)
        .skip((pag.page - 1) * pag.size)
        .limit(pag.size)
    )

    # Get total count
    count = await user_col.count_documents(filters)

    # Format
    data = [res async for res in results]

    return {
        "data": data,
        "meta": await get_pagination_metadata_mongo(
            total_count=count, count=len(data), page=pag.page, size=pag.size
        ),
    }


@router.put(
    "/{user_id}/",
    summary="Edit user obj",
    response_description="The new details of the user",
    status_code=200,
    response_model=schemas.UserResponse,
)
async def route_user_edit(user_id: UUID4, user_in: schemas.UserEdit):
    """
    This endpoint is used to edit user details
    """

    # Get user obj
    user = cast(schemas.UserDocument, await selectors.get_user_by_id(id=user_id))

    # Get col
    user_col = db.get_user_collection()

    # Update in DB
    await user_col.update_one(
        {"id": user["id"]},
        {"$set": {"first_name": user_in.first_name, "last_name": user_in.last_name}},
    )
    for field, value in user_in.model_dump().items():
        user[field] = value

    return {"data": user}


@router.delete(
    "/{user_id}/",
    summary="Delete user",
    response_description="User deleted successfully",
    status_code=200,
    response_model=ResponseSchema,
)
async def route_user_delete(user_id: UUID4):
    """
    This endpoint is used to edit a user obj
    """

    # Get user
    await selectors.get_user_by_id(id=user_id)

    # Get col
    user_col = db.get_user_collection()

    # Delete user
    await user_col.delete_one({"id": str(user_id)})

    return {"msg": "User has been deleted successfully", "data": None}
