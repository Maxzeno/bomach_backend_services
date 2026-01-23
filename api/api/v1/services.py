from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError

from api.api.schema.schemas import ServiceIn, ServiceOut, ServiceUpdate
from api.api.schema.others import MessageSchema
from api.models.service import Service


router = Router(tags=["Services"])


@router.get("", response=List[ServiceOut])
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


@router.post("", response={201: ServiceOut, 400: MessageSchema})
def create_service(request, payload: ServiceIn):
    try:
        service = Service.objects.create(**payload.dict())
        return 201, service
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{service_id}", response=ServiceOut)
def get_service(request, service_id: int):
    return get_object_or_404(Service.objects.select_related('category'), id=service_id)


@router.put("/{service_id}", response={200: ServiceOut, 400: MessageSchema, 404: MessageSchema})
def update_service(request, service_id: int, payload: ServiceUpdate):
    try:
        service = get_object_or_404(Service, id=service_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(service, attr, value)
        service.save()
        return 200, service
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{service_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_service(request, service_id: int):
    try:
        service = get_object_or_404(Service, id=service_id)
        service.delete()
        return 200, {"detail": "Service deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
