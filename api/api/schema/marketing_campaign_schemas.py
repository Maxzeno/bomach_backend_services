from ninja import Schema
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class MarketingCampaignIn(Schema):
    name: str
    description: Optional[str] = None
    status: str = "draft"
    channel: str
    impressions: int = 0
    ctr: Decimal = Decimal("0.00")
    roi: Decimal = Decimal("0.00")
    budget_allocated: Decimal
    budget_spent: Decimal = Decimal("0.00")
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class MarketingCampaignUpdate(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    channel: Optional[str] = None
    impressions: Optional[int] = None
    ctr: Optional[Decimal] = None
    roi: Optional[Decimal] = None
    budget_allocated: Optional[Decimal] = None
    budget_spent: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class MarketingCampaignOut(Schema):
    id: int
    name: str
    description: Optional[str]
    status: str
    channel: str
    impressions: int
    ctr: Decimal
    roi: Decimal
    progress_percentage: Decimal
    budget_allocated: Decimal
    budget_spent: Decimal
    budget_remaining: Decimal
    budget_utilization_percentage: float
    is_over_budget: bool
    clicks: int
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime


class MarketingCampaignListOut(Schema):
    count: int
    results: List[MarketingCampaignOut]
