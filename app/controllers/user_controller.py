from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services import user_service
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
        return await user_service.get_users()
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


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
        return await user_service.get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


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
        return user_service.add_user(user_data)
    except ValueError as e:
        return HTTPException(status_code=400, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


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
        return await user_service.update_user(user_id, updated_data)
    except ValueError as e:
        return HTTPException(status_code=400, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


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
        return await user_service.delete_user(user_id)
    except ValueError as e:
        return HTTPException(status_code=400, detail=e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)