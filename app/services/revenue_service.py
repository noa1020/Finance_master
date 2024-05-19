from app.database import repository
from app.database.db_connection import Collections
from app.models.revenue import Revenue
from app.services import validation_service


async def get_revenues():
    """
    Retrieve all revenues from the database.
    Returns:
        list: A list of revenue documents from the database.
    Raises:
        Exception: If there is an error during the retrieval process.
    """
    try:
        return await repository.get_all(Collections.revenues)
    except Exception as e:
        raise e


async def get_revenue_by_id(revenue_id: int):
    """
    Retrieve a revenue entry by its ID.
    Args:
        revenue_id (int): The ID of the revenue entry to retrieve.
    Returns:
        dict: The revenue document if found.
    Raises:
        ValueError: If the revenue entry is not found.
        Exception: If there is an error during the retrieval process.
    """
    try:
        revenue = await repository.get_by_id(Collections.revenues, revenue_id)
        if not revenue:
            raise ValueError(f"Revenue with ID {revenue_id} not found")
        return revenue
    except Exception as e:
        raise e


async def add_revenue(new_revenue: Revenue):
    """
    Add a new revenue entry to the database.
    Args:
        new_revenue (Revenue): The revenue object to add.
    Returns:
        dict: The added revenue document.
    Raises:
        ValueError: If the revenue object is null or the revenue ID already exists.
        Exception: If there is an error during the addition process.
    """
    if new_revenue is None:
        raise ValueError("Revenue object is null")
    if await get_revenue_by_id(new_revenue.id) is not None:
        raise ValueError("Revenue ID already exists")
    try:
        validation_service.is_valid_revenue(new_revenue)
        return await repository.add(Collections.revenues, new_revenue.dict())
    except Exception as e:
        raise e


async def update_revenue(revenue_id: int, updated_data: Revenue):
    """
    Update an existing revenue entry's data.
    Args:
        revenue_id (int): The ID of the revenue entry to update.
        updated_data (Revenue): The updated revenue object.
    Returns:
        dict: The updated revenue document.
    Raises:
        ValueError: If the revenue object is null or the revenue entry is not found.
        Exception: If there is an error during the update process.
    """
    if updated_data is None:
        raise ValueError("Revenue object is null")
    if await get_revenue_by_id(updated_data.id) is None:
        raise ValueError("Revenue not found")
    try:
        validation_service.is_valid_revenue(updated_data)
        return await repository.update(Collections.revenues, revenue_id, updated_data.dict())
    except Exception as e:
        raise e


async def delete_revenue(revenue_id: int):
    """
    Delete a revenue entry from the database.
    Args:
        revenue_id (int): The ID of the revenue entry to delete.
    Returns:
        dict: The deleted revenue document.
    Raises:
        ValueError: If the revenue entry is not found.
        Exception: If there is an error during the deletion process.
    """
    if await get_revenue_by_id(revenue_id) is None:
        raise ValueError("Revenue not found")
    try:
        return await repository.delete(Collections.revenues, revenue_id)
    except Exception as e:
        raise e