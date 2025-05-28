import math


async def get_pagination_metadata_mongo(
    *, total_count: int, count: int, page: int, size: int
) -> dict:
    """
    Generates pagination metadata for a MongoDB query result.

    Args:
        total_count (int): Total number of documents after filtering (from count_documents()).
        count (int): Number of items actually returned (after pagination).
        page (int): Current page number.
        size (int): Page size.

    Returns:
        dict: Pagination metadata.
    """
    total_pages = math.ceil(total_count / size) if size > 0 else 1

    return {
        "total_no_items": total_count,
        "total_no_pages": total_pages,
        "page": page,
        "size": size,
        "count": count,
        "has_next_page": page < total_pages,
        "has_prev_page": page > 1,
    }
