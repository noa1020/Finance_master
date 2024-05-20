from datetime import datetime
from pydantic import BaseModel


class Expense(BaseModel):

    id: int
    user_id: int
    amount: float
    date: datetime
    beneficiary: str
    documentation: str

