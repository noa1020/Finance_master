from fastapi import APIRouter, HTTPException
from app.utils import repositoy
from app.utils.db import Collections

user_router = APIRouter()


@user_router.get('')
async def get_users():
    """Routing that allows the user to access details about their expenses and revenues"""
    try:
        users = await repositoy.get_all(Collections.users)
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"oops... an error occurred in get users : {e}")
