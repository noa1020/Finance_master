from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    user_name: str
    email: str
    phone: str
    birth_date: datetime
