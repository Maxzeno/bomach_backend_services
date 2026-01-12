from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404

from api.api.schema.schemas import ServiceCategoryIn, ServiceCategoryOut
from api.models.service import ServiceCategory


router = Router()


@router.get("", response=List[ServiceCategoryOut], tags=["Categories"])
def list_categories(request):
    return ServiceCategory.objects.all()


@router.post("", response=ServiceCategoryOut, tags=["Categories"])
def create_category(request, payload: ServiceCategoryIn):
    category = ServiceCategory.objects.create(**payload.dict())
    return category


@router.get("/{category_id}", response=ServiceCategoryOut, tags=["Categories"])
def get_category(request, category_id: int):
    return get_object_or_404(ServiceCategory, id=category_id)


@router.put("/{category_id}", response=ServiceCategoryOut, tags=["Categories"])
def update_category(request, category_id: int, payload: ServiceCategoryIn):
    category = get_object_or_404(ServiceCategory, id=category_id)
    for attr, value in payload.dict().items():
        setattr(category, attr, value)
    category.save()
    return category


@router.delete("/{category_id}", tags=["Categories"])
def delete_category(request, category_id: int):
    category = get_object_or_404(ServiceCategory, id=category_id)
    category.delete()
    return {"success": True, "message": "Category deleted successfully"}
