import asyncio
from app.database import repository
from app.database.db_connection import Collections
from app.models.expense import Expense
from app.services import validation_service, balance_service, user_service


async def get_expenses(user_id: int):
    """
    Retrieve all expenses from the database for a specific user.
    Args:
        user_id (str): The ID of the user to retrieve expenses for.
    Returns:
        list: A list of expense documents from the database for the specified user.
    Raises:
        Exception: If there is an error during the retrieval process.
    """
    if await user_service.get_user_by_id(user_id) is None:
        raise ValueError("user not found")
    try:
        expenses = await repository.get_all(Collections.expenses)
        filtered_expenses = [expense for expense in expenses if expense.get('user_id') == user_id]
        return filtered_expenses
    except (ValueError, RuntimeError, Exception) as e:
        raise e


async def get_expense_by_id(expense_id: int, user_id: int):
    """
    Retrieve an expense entry by its ID.
    Args:
        expense_id (int): The ID of the expense entry to retrieve.
        user_id (int): The ID of the user requesting the expense.
    Returns:
        dict: The expense document if found.
    Raises:
        ValueError: If the expense entry is not found or if the user_id does not match.
        Exception: If there is an error during the retrieval process.
    """
    try:
        expense = await repository.get_by_id(Collections.expenses, expense_id)
        if user_id != expense['user_id']:
            raise ValueError("You are trying to access an expense of another user.")
        return expense
    except (ValueError, RuntimeError, Exception) as e:
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
    expenses = await repository.get_all(Collections.expenses)
    max_item = max(expenses, key=lambda item: item['id'])
    new_expense.id = max_item['id'] + 1
    try:
        validation_service.is_valid_expense(new_expense)
        results = await asyncio.gather(
            balance_service.change_balance(new_expense.user_id, -new_expense.amount),
            repository.add(Collections.expenses, new_expense.dict())
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
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
    existing_expense = await get_expense_by_id(new_expense.id, new_expense.user_id)
    if existing_expense is None:
        raise ValueError("Expense not found")
    existing_expense = Expense(**existing_expense)
    balance = existing_expense.amount - new_expense.amount
    try:
        update_expense_properties(existing_expense, new_expense)
        validation_service.is_valid_expense(existing_expense)
        results = await asyncio.gather(
            balance_service.change_balance(new_expense.user_id, balance),
            repository.update(Collections.expenses, expense_id, existing_expense.dict())
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
        raise e


async def delete_expense(expense_id: int, user_id: int):
    """
    Delete an expense entry from the database.
    Args:
        expense_id (int): The ID of the expense entry to delete.
        user_id (int): The ID of the user requesting the deletion.
    Returns:
        dict: The deleted expense document.
    Raises:
        ValueError: If the expense entry is not found or belongs to another user.
        Exception: If there is an error during the deletion process.
    """
    try:
        existing_expense = await get_expense_by_id(expense_id, user_id)
        if existing_expense is None:
            raise ValueError("Expense not found")
        existing_expense = Expense(**existing_expense)
        results = await asyncio.gather(
            balance_service.change_balance(existing_expense.user_id, existing_expense.amount),
            repository.delete(Collections.expenses, expense_id)
        )
        return results[1]
    except (ValueError, RuntimeError, Exception) as e:
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
