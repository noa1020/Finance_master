from datetime import datetime
from pydantic import BaseModel


class Expense(BaseModel):

    id: int
    user_id: str
    amount: float
    date: datetime
    beneficiary: str
    documentation: str

