from datetime import datetime
from pydantic import BaseModel


class Revenue(BaseModel):

    id: int
    userId: int
    amount: float
    date: datetime
    benefactor: str
    documentation: str
