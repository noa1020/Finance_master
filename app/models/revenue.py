from datetime import datetime
from pydantic import BaseModel


class Revenue(BaseModel):

    id: int
    user_id: int
    amount: float
    date: datetime
    benefactor: str
    documentation: str
