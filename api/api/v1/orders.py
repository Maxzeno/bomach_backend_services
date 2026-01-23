from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from api.api.schema.schemas import ServiceOrderIn, ServiceOrderOut, ServiceOrderUpdate
from api.api.schema.others import MessageSchema
from api.models.service import ServiceOrder
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Service Orders"])


@router.get("", response=List[ServiceOrderOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_orders(request, order_status: str = None, payment_status: str = None, client_id: str = None):
    """List all service orders with optional filtering."""
    orders = ServiceOrder.objects.select_related(
        'service', 'service__category', 'quote'
    ).all()

    if order_status:
        orders = orders.filter(order_status=order_status)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)
    if client_id:
        orders = orders.filter(client_id=client_id)

    return orders


@router.post("", response={201: ServiceOrderOut, 400: MessageSchema})
def create_order(request, payload: ServiceOrderIn):
    """Create a new service order."""
    try:
        order = ServiceOrder.objects.create(**payload.dict())
        return 201, order
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{order_id}", response=ServiceOrderOut)
def get_order(request, order_id: int):
    """Get a specific service order by ID."""
    return get_object_or_404(
        ServiceOrder.objects.select_related('service', 'service__category', 'quote'),
        id=order_id
    )


@router.put("/{order_id}", response={200: ServiceOrderOut, 400: MessageSchema, 404: MessageSchema})
def update_order(request, order_id: int, payload: ServiceOrderUpdate):
    """Update an existing service order."""
    try:
        order = get_object_or_404(ServiceOrder, id=order_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(order, attr, value)
        order.save()
        return 200, order
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{order_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_order(request, order_id: int):
    """Delete a service order."""
    try:
        order = get_object_or_404(ServiceOrder, id=order_id)
        order.delete()
        return 200, {"detail": "Order deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
