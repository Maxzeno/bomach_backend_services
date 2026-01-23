from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from api.api.schema.schemas import PaymentIn, PaymentOut
from api.api.schema.others import MessageSchema
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


@router.post("", response={201: PaymentOut, 400: MessageSchema})
def create_payment(request, payload: PaymentIn):
    try:
        payment = Payment.objects.create(**payload.dict())
        return 201, payment
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{payment_id}", response=PaymentOut)
def get_payment(request, payment_id: int):
    return get_object_or_404(Payment, id=payment_id)


@router.delete("/{payment_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_payment(request, payment_id: int):
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()
        return 200, {"detail": "Payment deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
