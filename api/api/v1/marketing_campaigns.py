from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Avg, Count
from ninja.pagination import paginate, LimitOffsetPagination

from api.api.schema.marketing_campaign_schemas import (
    MarketingCampaignIn,
    MarketingCampaignOut,
    MarketingCampaignUpdate
)
from api.models.marketing_campaign import MarketingCampaign


router = Router(tags=["Marketing Campaigns"])


@router.get("", response=List[MarketingCampaignOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_campaigns(
    request,
    status: str = None,
    channel: str = None,
    search: str = None
):
    """List all marketing campaigns with optional filtering."""
    campaigns = MarketingCampaign.objects.all()

    if status:
        campaigns = campaigns.filter(status=status)
    if channel:
        campaigns = campaigns.filter(channel=channel)
    if search:
        campaigns = campaigns.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return campaigns


@router.post("", response=MarketingCampaignOut)
def create_campaign(request, payload: MarketingCampaignIn):
    """Create a new marketing campaign."""
    campaign = MarketingCampaign.objects.create(**payload.dict())
    return campaign


@router.get("/{campaign_id}", response=MarketingCampaignOut)
def get_campaign(request, campaign_id: int):
    """Get a specific marketing campaign by ID."""
    return get_object_or_404(MarketingCampaign, id=campaign_id)


@router.put("/{campaign_id}", response=MarketingCampaignOut)
def update_campaign(request, campaign_id: int, payload: MarketingCampaignUpdate):
    """Update an existing marketing campaign."""
    campaign = get_object_or_404(MarketingCampaign, id=campaign_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(campaign, attr, value)
    campaign.save()
    return campaign


@router.delete("/{campaign_id}")
def delete_campaign(request, campaign_id: int):
    """Delete a marketing campaign."""
    campaign = get_object_or_404(MarketingCampaign, id=campaign_id)
    campaign.delete()
    return {"success": True, "message": "Marketing campaign deleted successfully"}


@router.get("/status/{status}/campaigns", response=List[MarketingCampaignOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_campaigns_by_status(request, status: str):
    """Get all campaigns with a specific status."""
    campaigns = MarketingCampaign.objects.filter(status=status)
    return campaigns


@router.get("/channel/{channel}/campaigns", response=List[MarketingCampaignOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_campaigns_by_channel(request, channel: str):
    """Get all campaigns for a specific channel."""
    campaigns = MarketingCampaign.objects.filter(channel=channel)
    return campaigns
