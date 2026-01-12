from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from api.api.schema.schemas import QuoteIn, QuoteOut, QuoteUpdate
from api.models.service import Quote
from ninja.pagination import paginate, LimitOffsetPagination


router = Router(tags=["Quotes"])


@router.get("", response=List[QuoteOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_quotes(request, status: str = None, client_id: str = None):
    """List all quotes with optional filtering."""
    quotes = Quote.objects.select_related('service', 'service__category').all()

    if status:
        quotes = quotes.filter(status=status)
    if client_id:
        quotes = quotes.filter(client_id=client_id)

    return quotes


@router.post("", response=QuoteOut)
def create_quote(request, payload: QuoteIn):
    """Create a new quote."""
    quote = Quote.objects.create(**payload.dict())
    return quote


@router.get("/{quote_id}", response=QuoteOut)
def get_quote(request, quote_id: int):
    """Get a specific quote by ID."""
    return get_object_or_404(
        Quote.objects.select_related('service', 'service__category'),
        id=quote_id
    )


@router.put("/{quote_id}", response=QuoteOut)
def update_quote(request, quote_id: int, payload: QuoteUpdate):
    """Update an existing quote."""
    quote = get_object_or_404(Quote, id=quote_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(quote, attr, value)
    quote.save()
    return quote


@router.delete("/{quote_id}")
def delete_quote(request, quote_id: int):
    """Delete a quote."""
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    return {"success": True, "message": "Quote deleted successfully"}
