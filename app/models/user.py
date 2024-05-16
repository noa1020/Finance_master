from pydantic import BaseModel


class User(BaseModel):
    userId: int
    userName: str
    email: str
