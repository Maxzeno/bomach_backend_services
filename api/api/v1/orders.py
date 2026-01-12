from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404

from api.api.schema.schemas import ServiceOrderIn, ServiceOrderOut, ServiceOrderUpdate
from api.models.service import ServiceOrder


router = Router()


@router.get("", response=List[ServiceOrderOut], tags=["Service Orders"])
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


@router.post("", response=ServiceOrderOut, tags=["Service Orders"])
def create_order(request, payload: ServiceOrderIn):
    """Create a new service order."""
    order = ServiceOrder.objects.create(**payload.dict())
    return order


@router.get("/{order_id}", response=ServiceOrderOut, tags=["Service Orders"])
def get_order(request, order_id: int):
    """Get a specific service order by ID."""
    return get_object_or_404(
        ServiceOrder.objects.select_related('service', 'service__category', 'quote'),
        id=order_id
    )


@router.put("/{order_id}", response=ServiceOrderOut, tags=["Service Orders"])
def update_order(request, order_id: int, payload: ServiceOrderUpdate):
    """Update an existing service order."""
    order = get_object_or_404(ServiceOrder, id=order_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(order, attr, value)
    order.save()
    return order


@router.delete("/{order_id}", tags=["Service Orders"])
def delete_order(request, order_id: int):
    """Delete a service order."""
    order = get_object_or_404(ServiceOrder, id=order_id)
    order.delete()
    return {"success": True, "message": "Order deleted successfully"}
