from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from api.api.schema.schemas import QuoteIn, QuoteOut, QuoteUpdate
from api.api.schema.others import MessageSchema
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


@router.post("", response={201: QuoteOut, 400: MessageSchema})
def create_quote(request, payload: QuoteIn):
    """Create a new quote."""
    try:
        quote = Quote.objects.create(**payload.dict())
        return 201, quote
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{quote_id}", response=QuoteOut)
def get_quote(request, quote_id: int):
    """Get a specific quote by ID."""
    return get_object_or_404(
        Quote.objects.select_related('service', 'service__category'),
        id=quote_id
    )


@router.put("/{quote_id}", response={200: QuoteOut, 400: MessageSchema, 404: MessageSchema})
def update_quote(request, quote_id: int, payload: QuoteUpdate):
    """Update an existing quote."""
    try:
        quote = get_object_or_404(Quote, id=quote_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(quote, attr, value)
        quote.save()
        return 200, quote
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{quote_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_quote(request, quote_id: int):
    """Delete a quote."""
    try:
        quote = get_object_or_404(Quote, id=quote_id)
        quote.delete()
        return 200, {"detail": "Quote deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}
