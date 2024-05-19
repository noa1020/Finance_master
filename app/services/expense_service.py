from app.database import repository
from app.database.db_connection import Collections
from app.models.expense import Expense
from app.services import validation_service


async def get_expenses():
    """
    Retrieve all expenses from the database.
    Returns:
        list: A list of expense documents from the database.
    Raises:
        Exception: If there is an error during the retrieval process.
    """
    try:
        return await repository.get_all(Collections.expenses)
    except Exception as e:
        raise e


async def get_expense_by_id(expense_id: int):
    """
    Retrieve an expense entry by its ID.
    Args:
        expense_id (int): The ID of the expense entry to retrieve.
    Returns:
        dict: The expense document if found.
    Raises:
        ValueError: If the expense entry is not found.
        Exception: If there is an error during the retrieval process.
    """
    try:
        expense = await repository.get_by_id(Collections.expenses, expense_id)
        if not expense:
            raise ValueError(f"Expense with ID {expense_id} not found")
        return expense
    except Exception as e:
        raise e


async def add_expense(new_expense: Expense):
    """
    Add a new expense entry to the database.
    Args:
        new_expense (Expense): The expense object to add.
    Returns:
        dict: The added expense document.
    Raises:
        ValueError: If the expense object is null or the expense ID already exists.
        Exception: If there is an error during the addition process.
    """
    if new_expense is None:
        raise ValueError("Expense object is null")
    if await get_expense_by_id(new_expense.id) is not None:
        raise ValueError("Expense ID already exists")
    try:
        validation_service.is_valid_expense(new_expense)
        return await repository.add(Collections.expenses, new_expense.dict())
    except Exception as e:
        raise e


async def update_expense(expense_id: int, updated_data: Expense):
    """
    Update an existing expense entry's data.
    Args:
        expense_id (int): The ID of the expense entry to update.
        updated_data (Expense): The updated expense object.
    Returns:
        dict: The updated expense document.
    Raises:
        ValueError: If the expense object is null or the expense entry is not found.
        Exception: If there is an error during the update process.
    """
    if updated_data is None:
        raise ValueError("Expense object is null")
    if await get_expense_by_id(updated_data.id) is None:
        raise ValueError("Expense not found")
    try:
        validation_service.is_valid_expense(updated_data)
        return await repository.update(Collections.expenses, expense_id, updated_data.dict())
    except Exception as e:
        raise e


async def delete_expense(expense_id: int):
    """
    Delete an expense entry from the database.
    Args:
        expense_id (int): The ID of the expense entry to delete.
    Returns:
        dict: The deleted expense document.
    Raises:
        ValueError: If the expense entry is not found.
        Exception: If there is an error during the deletion process.
    """
    if await get_expense_by_id(expense_id) is None:
        raise ValueError("Expense not found")
    try:
        return await repository.delete(Collections.expenses, expense_id)
    except Exception as e:
        raise e
