from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import ServiceLead
from ..schemas import ServiceLeadIn, ServiceLeadUpdate, ServiceLeadOut

router = Router()


@router.get("", response=List[ServiceLeadOut], tags=["Service Leads"])
def list_leads(request, status: str = None, client_id: str = None, search: str = None):
    """List all service leads with optional filtering."""
    leads = ServiceLead.objects.select_related('service', 'service__category').all()

    if status:
        leads = leads.filter(status=status)
    if client_id:
        leads = leads.filter(client_id=client_id)
    if search:
        leads = leads.filter(
            Q(client_name__icontains=search) | Q(notes__icontains=search)
        )

    return leads


@router.post("", response=ServiceLeadOut, tags=["Service Leads"])
def create_lead(request, payload: ServiceLeadIn):
    """Create a new service lead."""
    lead = ServiceLead.objects.create(**payload.dict())
    return lead


@router.get("/{lead_id}", response=ServiceLeadOut, tags=["Service Leads"])
def get_lead(request, lead_id: int):
    """Get a specific service lead by ID."""
    return get_object_or_404(
        ServiceLead.objects.select_related('service', 'service__category'),
        id=lead_id
    )


@router.put("/{lead_id}", response=ServiceLeadOut, tags=["Service Leads"])
def update_lead(request, lead_id: int, payload: ServiceLeadUpdate):
    """Update an existing service lead."""
    lead = get_object_or_404(ServiceLead, id=lead_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(lead, attr, value)
    lead.save()
    return lead


@router.delete("/{lead_id}", tags=["Service Leads"])
def delete_lead(request, lead_id: int):
    """Delete a service lead."""
    lead = get_object_or_404(ServiceLead, id=lead_id)
    lead.delete()
    return {"success": True, "message": "Lead deleted successfully"}
