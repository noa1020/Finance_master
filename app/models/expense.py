from datetime import datetime
from pydantic import BaseModel


class Expense(BaseModel):

    expenseId: int
    userId: int
    amount: str
    date: datetime
    beneficiary: str
    documentation: str

