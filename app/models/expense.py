from datetime import datetime
from pydantic import BaseModel


class Expense(BaseModel):

    expenseId: int
    userId: int
    amount: float
    date: datetime
    beneficiary: str
    documentation: str

