from pydantic import BaseModel


class User(BaseModel):
    id: int
    userName: str
    email: str
