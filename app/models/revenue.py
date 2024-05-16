from datetime import datetime
from pydantic import BaseModel


class Revenue(BaseModel):

    revenueId: int
    userId: int
    amount: str
    date: datetime
    benefactor: str
    documentation: str
