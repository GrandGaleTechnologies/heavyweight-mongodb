from typing import Annotated

from fastapi import Depends

from app.common.dependencies import pagination_params
from app.common.types import PaginationParamsType

PaginationParams = Annotated[PaginationParamsType, Depends(pagination_params)]
