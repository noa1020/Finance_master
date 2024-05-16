from fastapi import APIRouter, HTTPException
from app.utils import repository
from app.utils.db import Collections
from app.models.user import User
from flask import jsonify, Blueprint

user_router = APIRouter()


@user_router.get('')
async def get_users():
    """
    Retrieves details about all users from the database.

    Returns:
        list: A list of dictionaries, each representing a user.
    Raises:
        HTTPException: If an error occurs while fetching users from the database.
    """
    try:
        users = await repository.get_all(Collections.users)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while fetching users: {e}")


@user_router.get('/{user_id}')
async def get_user_by_id(user_id: int):
    """
    Retrieves details about a specific user by their ID from the database.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: A dictionary representing the user.
    Raises:
        HTTPException: If the specified user ID is not found or if an error occurs.
    """
    try:
        user = await repository.get_by_id(Collections.users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while fetching user: {e}")


@user_router.post('')
async def add_user(user_data: User):
    """
    Adds a new user to the database.

    Args:
        user_data (User): An instance of the User class representing the user to be added.

    Returns:
        dict: A dictionary representing the newly added user.
    Raises:
        HTTPException: If an error occurs while adding the user.
    """
    try:
        new_user = await repository.add(Collections.users, user_data.dict())
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while adding user: {e}")


@user_router.put('/{user_id}')
async def update_user(user_id: int, updated_data: User):
    """
    Updates an existing user in the database.

    Args:
        user_id (int): The ID of the user to update.
        updated_data (dict): A dictionary containing the updated user data.

    Returns:
        dict: A dictionary representing the updated user.
    Raises:
        HTTPException: If the specified user ID is not found or if an error occurs.
    """
    try:
        updated_user = await repository.update(Collections.users, user_id, updated_data.dict())
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while updating user: {e}")


@user_router.delete('/{user_id}')
async def delete_user(user_id: int):
    """
    Deletes an existing user from the database.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        dict: A dictionary representing the deleted user.
    Raises:
        HTTPException: If the specified user ID is not found or if an error occurs.
    """
    try:
        deleted_user = await repository.delete(Collections.users, user_id)
        return deleted_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while deleting user: {e}")
