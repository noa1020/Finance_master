from app.database import repository
from app.database.db_connection import Collections
from app.models.user import User
from app.services import validation_service


async def get_users():
    """
    Retrieve all users from the database.
    Returns:
        list: A list of user documents from the database.
    Raises:
        Exception: If there is an error during the retrieval process.
    """
    try:
        return await repository.get_all(Collections.users)
    except Exception as e:
        raise e


async def get_user_by_id(user_id: int):
    """
    Retrieve a user by their ID.
    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        dict: The user document if found.
    Raises:
        ValueError: If the user is not found.
        Exception: If there is an error during the retrieval process.
    """
    try:
        user = await repository.get_by_id(Collections.users, user_id)
        if not user:
            raise f"User with ID {user_id} not found"
        return user
    except Exception as e:
        raise e


async def add_user(new_user: User):
    """
    Add a new user to the database.
    Args:
        new_user (User): The user object to add.
    Returns:
        dict: The added user document.
    Raises:
        ValueError: If the user object is null or the user ID already exists.
        Exception: If there is an error during the addition process.
    """
    if new_user is None:
        raise ValueError("User object is null")
    if await get_user_by_id(new_user.id) is not None:
        raise ValueError("User ID already exists")
    try:
        validation_service.is_valid_user(new_user)
        return await repository.add(Collections.users, new_user.dict())
    except Exception as e:
        raise e


async def update_user(user_id: int, new_user: User):
    """
    Update an existing user's data.
    Args:
        user_id (int): The ID of the user to update.
        new_user (User): The updated user object.
    Returns:
        dict: The updated user document.
    Raises:
        ValueError: If the user object is null or the user is not found.
        Exception: If there is an error during the update process.
    """
    if new_user is None:
        raise ValueError("User object is null")
    existing_user = await get_user_by_id(new_user.id)
    if existing_user is None:
        raise ValueError("User not found")
    existing_user = User(**existing_user)
    try:
        update_user_properties(existing_user, new_user)
        validation_service.is_valid_user(existing_user)
        return await repository.update(Collections.users, user_id, existing_user.dict())
    except Exception as e:
        raise e


async def delete_user(user_id: int):
    """
    Delete a user from the database.
    Args:
        user_id (int): The ID of the user to delete.
    Returns:
        dict: The deleted user document.
    Raises:
        ValueError: If the user is not found.
        Exception: If there is an error during the deletion process.
    """
    if await get_user_by_id(user_id) is None:
        raise ValueError("User not found")
    try:
        return await repository.delete(Collections.users, user_id)
    except Exception as e:
        raise e


def update_user_properties(existing_user: User, new_user: User):
    """
    Updates the properties of an existing User object with values from a new User object.
    Args:
        existing_user (User): The existing User object to update.
        new_user (User): The new User object with updated values.
    Returns:
        None
    Raises:
        TypeError: If either existing_user or new_user is not an instance of the Expense class.
    """
    existing_user.user_name = new_user.user_name or existing_user.user_name
    existing_user.password = new_user.password or existing_user.password
    existing_user.email = new_user.email or existing_user.email
    existing_user.phone = new_user.phone or existing_user.phone
    existing_user.birth_date = new_user.birth_date or existing_user.birth_date
    existing_user.balance = new_user.balance or existing_user.balance
