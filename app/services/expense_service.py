from app.database import repository
from app.database.db_connection import Collections
from app.models.expense import Expense
from app.services import validation_service, balance_service


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
        return await repository.get_by_id(Collections.expenses, expense_id)
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
        await balance_service.change_balance(new_expense.userId, new_expense.amount)
        return await repository.add(Collections.expenses, new_expense.dict())
    except ValueError as ve:
        raise ValueError(ve)
    except Exception as e:
        raise e


async def update_expense(expense_id: int, new_expense: Expense):
    """
    Update an existing expense entry's data.
    Args:
        expense_id (int): The ID of the expense entry to update.
        new_expense (Expense): The updated expense object.
    Returns:
        dict: The updated expense document.
    Raises:
        ValueError: If the expense object is null or the expense entry is not found.
        Exception: If there is an error during the update process.
    """
    if new_expense is None:
        raise ValueError("Expense object is null")
    existing_expense = await get_expense_by_id(new_expense.id)
    if existing_expense is None:
        raise ValueError("Expense not found")
    existing_expense = Expense(**existing_expense)
    try:
        update_expense_properties(existing_expense, new_expense)
        validation_service.is_valid_expense(existing_expense)
        await balance_service.change_balance(new_expense.userId, new_expense.amount - existing_expense.amount)
        return await repository.update(Collections.expenses, expense_id, existing_expense.dict())
    except ValueError as ve:
        raise ValueError(ve)
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
    existing_expense = await get_expense_by_id(expense_id)
    if existing_expense is None:
        raise ValueError("Expense not found")
    existing_expense = Expense(**existing_expense)
    try:
        await balance_service.change_balance(existing_expense.userId, existing_expense.amount * -1)
        return await repository.delete(Collections.expenses, expense_id)
    except ValueError as ve:
        raise ValueError(ve)
    except Exception as e:
        raise e


def update_expense_properties(existing_expense: Expense, new_expense: Expense):
    """
    Updates the properties of an existing Expense object with values from a new Expense object.
    Args:
        existing_expense (Expense): The existing Expense object to update.
        new_expense (Expense): The new Expense object with updated values.
    Returns:
        None
    Raises:
        TypeError: If either existing_expense or new_expense is not an instance of the Expense class.
    """
    existing_expense.date = new_expense.date or new_expense.date
    existing_expense.amount = new_expense.amount or new_expense.amount
    existing_expense.beneficiary = new_expense.beneficiary or new_expense.beneficiary
    existing_expense.documentation = new_expense.documentation or new_expense.documentation
