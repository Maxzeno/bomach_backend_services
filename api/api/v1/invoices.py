from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError

from api.api.schema.schemas import InvoiceIn, InvoiceOut, InvoiceUpdate
from api.api.schema.others import MessageSchema
from api.models.payment import Invoice, InvoiceItem
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Invoices"])


@router.get("", response=List[InvoiceOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_invoices(request, status: str = None, client_id: str = None, search: str = None):
    """List all invoices with optional filtering."""
    invoices = Invoice.objects.select_related(
        'service', 'service__category', 'order', 'lead'
    ).prefetch_related('items').all()

    if status:
        invoices = invoices.filter(status=status)
    if client_id:
        invoices = invoices.filter(client_id=client_id)
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search) | Q(client_name__icontains=search)
        )

    return invoices


@router.post("", response={201: InvoiceOut, 400: MessageSchema})
def create_invoice(request, payload: InvoiceIn):
    """Create a new invoice with optional line items."""
    try:
        data = payload.dict()
        items_data = data.pop('items', [])
        invoice = Invoice.objects.create(**data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return 201, invoice
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{invoice_id}", response=InvoiceOut)
def get_invoice(request, invoice_id: int):
    """Get a specific invoice by ID."""
    return get_object_or_404(
        Invoice.objects.select_related(
            'service', 'service__category', 'order', 'lead'
        ).prefetch_related('items'),
        id=invoice_id
    )


@router.put("/{invoice_id}", response={200: InvoiceOut, 400: MessageSchema, 404: MessageSchema})
def update_invoice(request, invoice_id: int, payload: InvoiceUpdate):
    """Update an existing invoice."""
    try:
        invoice = get_object_or_404(Invoice, id=invoice_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(invoice, attr, value)
        invoice.save()
        return 200, invoice
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{invoice_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_invoice(request, invoice_id: int):
    """Delete an invoice."""
    try:
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.delete()
        return 200, {"detail": "Invoice deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
