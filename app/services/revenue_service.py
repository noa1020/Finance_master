import asyncio
from app.database import repository
from app.database.db_connection import Collections
from app.models.revenue import Revenue
from app.services import validation_service, balance_service, user_service


async def get_revenues(user_id: int):
    """
    Retrieve all revenues from the database for a specific user.
    Args:
        user_id (int): The ID of the user to retrieve revenues for.
    Returns:
        list: A list of revenue documents from the database for the specified user.
    Raises:
        Exception: If there is an error during the retrieval process.
    """
    if await user_service.get_user_by_id(user_id) is None:
        raise ValueError("User not found")
    try:
        revenues = await repository.get_all(Collections.revenues)
        filtered_revenues = [revenue for revenue in revenues if revenue.get('user_id') == user_id]
        return filtered_revenues
    except (ValueError, RuntimeError, Exception) as e:
        raise e


async def get_revenue_by_id(revenue_id: int, user_id: int):
    """
    Retrieve a revenue entry by its ID.
    Args:
        revenue_id (int): The ID of the revenue entry to retrieve.
        user_id (int): The ID of the user requesting the revenue.
    Returns:
        dict: The revenue document if found.
    Raises:
        ValueError: If the revenue entry is not found or if the user_id does not match.
        Exception: If there is an error during the retrieval process.
    """
    try:
        revenue = await repository.get_by_id(Collections.revenues, revenue_id)
        if user_id != revenue['user_id']:
            raise ValueError("You are trying to access revenue of another user.")
        return revenue
    except (ValueError, RuntimeError, Exception) as e:
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
    revenues = await repository.get_all(Collections.revenues)
    max_item = max(revenues, key=lambda item: item['id'])
    new_revenue.id = max_item['id'] + 1
    try:
        validation_service.is_valid_revenue(new_revenue)
        results = await asyncio.gather(
            balance_service.change_balance(new_revenue.user_id, new_revenue.amount),
            repository.add(Collections.revenues, new_revenue.dict())
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
        raise e


async def update_revenue(revenue_id: int, new_revenue: Revenue):
    """
    Update an existing revenue entry's data.
    Args:
        revenue_id (int): The ID of the revenue entry to update.
        new_revenue (Revenue): The updated revenue object.
    Returns:
        dict: The updated revenue document.
    Raises:
        ValueError: If the revenue object is null or the revenue entry is not found.
        Exception: If there is an error during the update process.
    """
    if new_revenue is None:
        raise ValueError("Revenue object is null")
    existing_revenue = await get_revenue_by_id(new_revenue.id, new_revenue.user_id)
    if existing_revenue is None:
        raise ValueError("Revenue not found")
    existing_revenue = Revenue(**existing_revenue)
    balance = new_revenue.amount - existing_revenue.amount
    try:
        update_revenue_properties(existing_revenue, new_revenue)
        validation_service.is_valid_revenue(existing_revenue)
        results = await asyncio.gather(
            balance_service.change_balance(new_revenue.user_id, balance),
            repository.update(Collections.revenues, revenue_id, existing_revenue.dict())
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
        raise e


async def delete_revenue(revenue_id: int, user_id: int):
    """
    Delete a revenue entry from the database.
    Args:
        revenue_id (int): The ID of the revenue entry to delete.
        user_id (int): The ID of the user requesting the deletion.
    Returns:
        dict: The deleted revenue document.
    Raises:
        ValueError: If the revenue entry is not found or belongs to another user.
        Exception: If there is an error during the deletion process.
    """
    try:
        existing_revenue = await get_revenue_by_id(revenue_id, user_id)
        if existing_revenue is None:
            raise ValueError("Revenue not found")
        existing_revenue = Revenue(**existing_revenue)
        results = await asyncio.gather(
            balance_service.change_balance(existing_revenue.user_id, -existing_revenue.amount),
            repository.delete(Collections.revenues, revenue_id)
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
        raise e


def update_revenue_properties(existing_revenue: Revenue, new_revenue: Revenue):
    """
    Updates the properties of an existing Revenue object with values from a new Revenue object.
    Args:
        existing_revenue (Revenue): The existing Revenue object to update.
        new_revenue (Revenue): The new Revenue object with updated values.
    Returns:
        None
    Raises:
        TypeError: If either existing_revenue or new_revenue is not an instance of the Revenue class.
    """
    existing_revenue.date = new_revenue.date or existing_revenue.date
    existing_revenue.amount = new_revenue.amount or existing_revenue.amount
    existing_revenue.benefactor = new_revenue.benefactor or existing_revenue.benefactor
    existing_revenue.documentation = new_revenue.documentation or existing_revenue.documentation
