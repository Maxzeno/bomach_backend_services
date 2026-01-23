from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from api.api.schema.schemas import ServiceCategoryIn, ServiceCategoryOut
from api.api.schema.others import MessageSchema
from api.models.service import ServiceCategory
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Categories"])


@router.get("", response=List[ServiceCategoryOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_categories(request):
    return ServiceCategory.objects.all()


@router.post("", response={201: ServiceCategoryOut, 400: MessageSchema})
def create_category(request, payload: ServiceCategoryIn):
    try:
        category = ServiceCategory.objects.create(**payload.dict())
        return 201, category
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{category_id}", response=ServiceCategoryOut)
def get_category(request, category_id: int):
    return get_object_or_404(ServiceCategory, id=category_id)


@router.put("/{category_id}", response={200: ServiceCategoryOut, 400: MessageSchema, 404: MessageSchema})
def update_category(request, category_id: int, payload: ServiceCategoryIn):
    try:
        category = get_object_or_404(ServiceCategory, id=category_id)
        for attr, value in payload.dict().items():
            setattr(category, attr, value)
        category.save()
        return 200, category
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{category_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_category(request, category_id: int):
    try:
        category = get_object_or_404(ServiceCategory, id=category_id)
        category.delete()
        return 200, {"detail": "Category deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
