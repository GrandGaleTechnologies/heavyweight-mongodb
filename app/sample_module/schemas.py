"""This module contains the pydantic models for the example module."""

from typing import TypedDict

from pydantic import UUID4, BaseModel, Field

from app.common.schemas import PaginatedResponseSchema


######################################################################
# User
######################################################################
class User(BaseModel):
    """
    Base schema for users
    """

    id: UUID4 = Field(description="The ID of the user")
    first_name: str = Field(description="The first name of the user")
    last_name: str = Field(description="The last name of the user")


class UserDocument(TypedDict):
    """
    Document schema for user docs
    """

    id: UUID4
    first_name: str
    last_name: str


class UserCreate(BaseModel):
    """
    Create schema for users
    """

    first_name: str = Field(description="The first name of the user")
    last_name: str = Field(description="The last name of the user")


class UserEdit(BaseModel):
    """
    Create schema for users
    """

    first_name: str = Field(description="The first name of the user")
    last_name: str = Field(description="The last name of the user")


class UserResponse(BaseModel):
    """
    Response schema for users
    """

    data: User = Field(description="The details of the user")


class PaginatedUserListResponse(PaginatedResponseSchema):
    """
    Paginated response schema for users
    """

    data: list[User] = Field(description="The list of names")
