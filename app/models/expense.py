from datetime import datetime
from pydantic import BaseModel


class Expense(BaseModel):

    id: int
    userId: int
    amount: float
    date: datetime
    beneficiary: str
    documentation: str

