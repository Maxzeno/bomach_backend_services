from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404

from api.api.schema.schemas import PaymentIn, PaymentOut
from api.models.payment import Payment
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Payments"])


@router.get("", response=List[PaymentOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_payments(request, invoice_id: int = None):
    payments = Payment.objects.all()

    if invoice_id:
        payments = payments.filter(invoice_id=invoice_id)

    return payments


@router.post("", response=PaymentOut)
def create_payment(request, payload: PaymentIn):
    payment = Payment.objects.create(**payload.dict())
    return payment


@router.get("/{payment_id}", response=PaymentOut)
def get_payment(request, payment_id: int):
    return get_object_or_404(Payment, id=payment_id)


@router.delete("/{payment_id}")
def delete_payment(request, payment_id: int):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return {"detail": "Payment deleted successfully"}
