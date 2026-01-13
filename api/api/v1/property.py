from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from ninja.pagination import paginate, LimitOffsetPagination

from api.api.schema.property_schemas import PropertyIn, PropertyOut, PropertyUpdate, PropertyStatsOut
from api.models.property import Property


router = Router(tags=["Properties"])


@router.get("/stats", response=PropertyStatsOut)
def get_property_stats(request):
    """Get property statistics for dashboard."""
    total = Property.objects.count()
    available = Property.objects.filter(status='available').count()
    reserved = Property.objects.filter(status='reserved').count()
    sold_rented = Property.objects.filter(Q(status='sold') | Q(status='rented')).count()

    for_sale = Property.objects.filter(category='sale').count()
    for_rent = Property.objects.filter(category='rent').count()
    for_lease = Property.objects.filter(category='lease').count()

    return {
        "total_properties": total,
        "available": available,
        "reserved": reserved,
        "sold_rented": sold_rented,
        "for_sale": for_sale,
        "for_rent": for_rent,
        "for_lease": for_lease
    }


@router.get("", response=List[PropertyOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_properties(
    request,
    category: str = None,
    status: str = None,
    client_id: str = None,
    search: str = None
):
    """List all properties with optional filtering."""
    properties = Property.objects.all()

    if category:
        properties = properties.filter(category=category)
    if status:
        properties = properties.filter(status=status)
    if client_id:
        properties = properties.filter(client_id=client_id)
    if search:
        properties = properties.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search) |
            Q(description__icontains=search)
        )

    return properties


@router.post("", response=PropertyOut)
def create_property(request, payload: PropertyIn):
    """Create a new property."""
    property = Property.objects.create(**payload.dict())
    return property


@router.get("/{property_id}", response=PropertyOut)
def get_property(request, property_id: int):
    """Get a specific property by ID."""
    return get_object_or_404(Property, id=property_id)


@router.put("/{property_id}", response=PropertyOut)
def update_property(request, property_id: int, payload: PropertyUpdate):
    """Update an existing property."""
    property = get_object_or_404(Property, id=property_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(property, attr, value)
    property.save()
    return property


@router.delete("/{property_id}")
def delete_property(request, property_id: int):
    """Delete a property."""
    property = get_object_or_404(Property, id=property_id)
    property.delete()
    return {"detail": "Property deleted successfully"}


@router.get("/client/{client_id}/properties", response=List[PropertyOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_client_properties(request, client_id: str):
    """Get all properties for a specific client."""
    properties = Property.objects.filter(client_id=client_id)
    return properties
