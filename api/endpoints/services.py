from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import Service
from ..schemas import ServiceIn, ServiceUpdate, ServiceOut

router = Router()


@router.get("", response=List[ServiceOut], tags=["Services"])
def list_services(request, status: str = None, category_id: int = None, search: str = None):
    services = Service.objects.select_related('category').all()

    if status:
        services = services.filter(status=status)
    if category_id:
        services = services.filter(category_id=category_id)
    if search:
        services = services.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return services


@router.post("", response=ServiceOut, tags=["Services"])
def create_service(request, payload: ServiceIn):
    service = Service.objects.create(**payload.dict())
    return service


@router.get("/{service_id}", response=ServiceOut, tags=["Services"])
def get_service(request, service_id: int):
    return get_object_or_404(Service.objects.select_related('category'), id=service_id)


@router.put("/{service_id}", response=ServiceOut, tags=["Services"])
def update_service(request, service_id: int, payload: ServiceUpdate):
    service = get_object_or_404(Service, id=service_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(service, attr, value)
    service.save()
    return service


@router.delete("/{service_id}", tags=["Services"])
def delete_service(request, service_id: int):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return {"success": True, "message": "Service deleted successfully"}
