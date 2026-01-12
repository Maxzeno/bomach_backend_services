from ninja import Schema
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class ExpenseIn(Schema):
    user_id: str
    date: date
    description: str
    amount: Decimal
    category: str = "other"
    status: str = "pending"


class ExpenseUpdate(Schema):
    user_id: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    category: Optional[str] = None
    status: Optional[str] = None


class ExpenseOut(Schema):
    id: int
    user_id: str
    date: date
    description: str
    amount: Decimal
    category: str
    status: str
    created_at: datetime
    updated_at: datetime


class ExpenseListOut(Schema):
    count: int
    results: List[ExpenseOut]
