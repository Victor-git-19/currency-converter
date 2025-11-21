# app/schemas.py
from pydantic import BaseModel


class ConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    amount: float
    converted: float
