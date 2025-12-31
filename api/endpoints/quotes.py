from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404

from ..models import Quote
from ..schemas import QuoteIn, QuoteUpdate, QuoteOut

router = Router()


@router.get("", response=List[QuoteOut], tags=["Quotes"])
def list_quotes(request, status: str = None, client_id: str = None):
    """List all quotes with optional filtering."""
    quotes = Quote.objects.select_related('service', 'service__category').all()

    if status:
        quotes = quotes.filter(status=status)
    if client_id:
        quotes = quotes.filter(client_id=client_id)

    return quotes


@router.post("", response=QuoteOut, tags=["Quotes"])
def create_quote(request, payload: QuoteIn):
    """Create a new quote."""
    quote = Quote.objects.create(**payload.dict())
    return quote


@router.get("/{quote_id}", response=QuoteOut, tags=["Quotes"])
def get_quote(request, quote_id: int):
    """Get a specific quote by ID."""
    return get_object_or_404(
        Quote.objects.select_related('service', 'service__category'),
        id=quote_id
    )


@router.put("/{quote_id}", response=QuoteOut, tags=["Quotes"])
def update_quote(request, quote_id: int, payload: QuoteUpdate):
    """Update an existing quote."""
    quote = get_object_or_404(Quote, id=quote_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(quote, attr, value)
    quote.save()
    return quote


@router.delete("/{quote_id}", tags=["Quotes"])
def delete_quote(request, quote_id: int):
    """Delete a quote."""
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    return {"success": True, "message": "Quote deleted successfully"}
