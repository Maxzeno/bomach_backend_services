from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Avg, Count
from ninja.pagination import paginate, LimitOffsetPagination
from django.utils import timezone
from django.core.exceptions import ValidationError

from api.api.schema.event_schemas import (
    EventIn,
    EventOut,
    EventUpdate,
    EventRegistrationIn,
    EventRegistrationOut,
    EventRegistrationUpdate
)
from api.api.schema.others import MessageSchema
from api.models.event import Event, EventRegistration


router = Router(tags=["Events"])


# Event CRUD Operations
@router.get("", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_events(
    request,
    status: str = None,
    event_type: str = None,
    is_online: bool = None,
    is_featured: bool = None,
    is_public: bool = None,
    organizer_id: str = None,
    search: str = None
):
    """List all events with optional filtering."""
    events = Event.objects.all()

    if status:
        events = events.filter(status=status)
    if event_type:
        events = events.filter(event_type=event_type)
    if is_online is not None:
        events = events.filter(is_online=is_online)
    if is_featured is not None:
        events = events.filter(is_featured=is_featured)
    if is_public is not None:
        events = events.filter(is_public=is_public)
    if organizer_id:
        events = events.filter(organizer_id=organizer_id)
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(venue_name__icontains=search) |
            Q(city__icontains=search) |
            Q(tags__icontains=search)
        )

    return events


@router.post("", response={201: EventOut, 400: MessageSchema})
def create_event(request, payload: EventIn):
    """Create a new event."""
    try:
        event = Event.objects.create(**payload.dict())
        return 201, event
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{event_id}", response=EventOut)
def get_event(request, event_id: int):
    """Get a specific event by ID."""
    return get_object_or_404(Event, id=event_id)


@router.put("/{event_id}", response={200: EventOut, 400: MessageSchema, 404: MessageSchema})
def update_event(request, event_id: int, payload: EventUpdate):
    """Update an existing event."""
    try:
        event = get_object_or_404(Event, id=event_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(event, attr, value)
        event.save()
        return 200, event
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/{event_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_event(request, event_id: int):
    """Delete an event."""
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return 200, {"detail": "Event deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


# Event Filtered Views
@router.get("/upcoming/all", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_upcoming_events(request):
    """Get all upcoming events."""
    events = Event.objects.filter(event_date__gte=timezone.now().date()).order_by('event_date', 'start_time')
    return events


@router.get("/past/all", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_past_events(request):
    """Get all past events."""
    events = Event.objects.filter(event_date__lt=timezone.now().date()).order_by('-event_date', '-start_time')
    return events


@router.get("/featured/all", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_featured_events(request):
    """Get all featured events."""
    events = Event.objects.filter(is_featured=True)
    return events


@router.get("/type/{event_type}/events", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_events_by_type(request, event_type: str):
    """Get all events of a specific type."""
    events = Event.objects.filter(event_type=event_type)
    return events


@router.get("/organizer/{organizer_id}/events", response=List[EventOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_organizer_events(request, organizer_id: str):
    """Get all events by a specific organizer."""
    events = Event.objects.filter(organizer_id=organizer_id)
    return events


# Event Registration Management
@router.post("/{event_id}/increment-registration", response=EventOut)
def increment_event_registration(request, event_id: int):
    """Increment registration count for an event."""
    event = get_object_or_404(Event, id=event_id)
    if event.increment_registrations():
        return event
    return {"detail": "Event is full"}


@router.post("/{event_id}/decrement-registration", response=EventOut)
def decrement_event_registration(request, event_id: int):
    """Decrement registration count for an event."""
    event = get_object_or_404(Event, id=event_id)
    if event.decrement_registrations():
        return event
    return {"detail": "No registrations to decrement"}


# EventRegistration CRUD Operations
@router.get("/registrations/all", response=List[EventRegistrationOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_registrations(
    request,
    event_id: int = None,
    attendee_id: str = None,
    status: str = None,
    payment_status: str = None
):
    """List all event registrations with optional filtering."""
    registrations = EventRegistration.objects.select_related('event').all()

    if event_id:
        registrations = registrations.filter(event_id=event_id)
    if attendee_id:
        registrations = registrations.filter(attendee_id=attendee_id)
    if status:
        registrations = registrations.filter(status=status)
    if payment_status:
        registrations = registrations.filter(payment_status=payment_status)

    return registrations


@router.post("/registrations", response={201: EventRegistrationOut, 400: MessageSchema, 404: MessageSchema})
def create_registration(request, payload: EventRegistrationIn):
    """Create a new event registration."""
    try:
        event = get_object_or_404(Event, id=payload.event_id)

        # Check if event is full
        if event.is_full:
            return 400, {"detail": "Event is full"}

        # Check if registration is allowed
        if not event.allow_registration:
            return 400, {"detail": "Registration is not allowed for this event"}

        # Create registration
        registration = EventRegistration.objects.create(
            event=event,
            attendee_id=payload.attendee_id,
            status=payload.status,
            payment_status=payload.payment_status,
            notes=payload.notes
        )

        # Increment event registration count
        event.increment_registrations()

        return 201, registration
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/registrations/{registration_id}", response=EventRegistrationOut)
def get_registration(request, registration_id: int):
    """Get a specific event registration by ID."""
    return get_object_or_404(EventRegistration.objects.select_related('event'), id=registration_id)


@router.put("/registrations/{registration_id}", response={200: EventRegistrationOut, 400: MessageSchema, 404: MessageSchema})
def update_registration(request, registration_id: int, payload: EventRegistrationUpdate):
    """Update an existing event registration."""
    try:
        registration = get_object_or_404(EventRegistration, id=registration_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(registration, attr, value)
        registration.save()
        return 200, registration
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.delete("/registrations/{registration_id}", response={200: MessageSchema, 400: MessageSchema, 404: MessageSchema})
def delete_registration(request, registration_id: int):
    """Delete an event registration."""
    try:
        registration = get_object_or_404(EventRegistration, id=registration_id)
        event = registration.event
        registration.delete()

        # Decrement event registration count
        event.decrement_registrations()

        return 200, {"detail": "Registration deleted successfully"}
    except ValidationError as e:
        return 400, {'detail': e.messages[0]}
    except Exception as e:
        return 400, {'detail': str(e)}


@router.get("/{event_id}/registrations", response=List[EventRegistrationOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_event_registrations(request, event_id: int):
    """Get all registrations for a specific event."""
    registrations = EventRegistration.objects.filter(event_id=event_id)
    return registrations


@router.get("/registrations/confirmation/{confirmation_code}", response=EventRegistrationOut)
def get_registration_by_confirmation(request, confirmation_code: str):
    """Get registration by confirmation code."""
    return get_object_or_404(EventRegistration.objects.select_related('event'), confirmation_code=confirmation_code)


@router.get("/attendee/{attendee_id}/registrations", response=List[EventRegistrationOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_attendee_registrations(request, attendee_id: str):
    """Get all registrations for a specific attendee."""
    registrations = EventRegistration.objects.filter(attendee_id=attendee_id).select_related('event')
    return registrations
