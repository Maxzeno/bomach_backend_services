from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..models import Invoice, InvoiceItem
from ..schemas import InvoiceIn, InvoiceUpdate, InvoiceOut

router = Router()


@router.get("", response=List[InvoiceOut], tags=["Invoices"])
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


@router.post("", response=InvoiceOut, tags=["Invoices"])
def create_invoice(request, payload: InvoiceIn):
    """Create a new invoice with optional line items."""
    data = payload.dict()
    items_data = data.pop('items', [])
    invoice = Invoice.objects.create(**data)

    for item_data in items_data:
        InvoiceItem.objects.create(invoice=invoice, **item_data)

    return invoice


@router.get("/{invoice_id}", response=InvoiceOut, tags=["Invoices"])
def get_invoice(request, invoice_id: int):
    """Get a specific invoice by ID."""
    return get_object_or_404(
        Invoice.objects.select_related(
            'service', 'service__category', 'order', 'lead'
        ).prefetch_related('items'),
        id=invoice_id
    )


@router.put("/{invoice_id}", response=InvoiceOut, tags=["Invoices"])
def update_invoice(request, invoice_id: int, payload: InvoiceUpdate):
    """Update an existing invoice."""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(invoice, attr, value)
    invoice.save()
    return invoice


@router.delete("/{invoice_id}", tags=["Invoices"])
def delete_invoice(request, invoice_id: int):
    """Delete an invoice."""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return {"success": True, "message": "Invoice deleted successfully"}
