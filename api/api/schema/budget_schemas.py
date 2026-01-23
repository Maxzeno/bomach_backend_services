from ninja import Schema
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class BudgetIn(Schema):
    invoice_id: int
    project_id: str
    budget_date: date
    amount: Decimal
    payment_method: str = "transfer"
    status: str = "draft"


class BudgetUpdate(Schema):
    invoice_id: Optional[int] = None
    project_id: Optional[str] = None
    budget_date: Optional[date] = None
    amount: Optional[Decimal] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None


class BudgetOut(Schema):
    id: int
    invoice_id: int
    project_id: str
    budget_date: date
    amount: Decimal
    amount_display: str
    payment_method: str
    status: str
    created_at: datetime
    updated_at: datetime


class BudgetListOut(Schema):
    count: int
    results: List[BudgetOut]
