from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Avg, Count
from ninja.pagination import paginate, LimitOffsetPagination

from api.api.schema.content_schemas import (
    ContentIn,
    ContentOut,
    ContentUpdate
)
from api.models.content import Content


router = Router(tags=["Content"])


@router.get("", response=List[ContentOut])
@paginate(LimitOffsetPagination, page_size=10)
def list_content(
    request,
    status: str = None,
    content_type: str = None,
    platform: str = None,
    author_id: str = None,
    is_featured: bool = None,
    search: str = None
):
    """List all content with optional filtering."""
    contents = Content.objects.all()

    if status:
        contents = contents.filter(status=status)
    if content_type:
        contents = contents.filter(content_type=content_type)
    if platform:
        contents = contents.filter(platform=platform)
    if author_id:
        contents = contents.filter(author_id=author_id)
    if is_featured is not None:
        contents = contents.filter(is_featured=is_featured)
    if search:
        contents = contents.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(tags__icontains=search)
        )

    return contents


@router.post("", response=ContentOut)
def create_content(request, payload: ContentIn):
    """Create new content."""
    content = Content.objects.create(**payload.dict())
    return content


@router.get("/{content_id}", response=ContentOut)
def get_content(request, content_id: int):
    """Get a specific content by ID."""
    return get_object_or_404(Content, id=content_id)


@router.put("/{content_id}", response=ContentOut)
def update_content(request, content_id: int, payload: ContentUpdate):
    """Update existing content."""
    content = get_object_or_404(Content, id=content_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(content, attr, value)
    content.save()
    return content


@router.delete("/{content_id}")
def delete_content(request, content_id: int):
    """Delete content."""
    content = get_object_or_404(Content, id=content_id)
    content.delete()
    return {"detail": "Content deleted successfully"}


@router.get("/slug/{slug}", response=ContentOut)
def get_content_by_slug(request, slug: str):
    """Get content by slug."""
    return get_object_or_404(Content, slug=slug)


@router.get("/author/{author_id}/content", response=List[ContentOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_author_content(request, author_id: str):
    """Get all content by a specific author."""
    contents = Content.objects.filter(author_id=author_id)
    return contents


@router.get("/platform/{platform}/content", response=List[ContentOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_platform_content(request, platform: str):
    """Get all content for a specific platform."""
    contents = Content.objects.filter(platform=platform)
    return contents


@router.post("/{content_id}/increment-views", response=ContentOut)
def increment_views(request, content_id: int):
    """Increment view count for content."""
    content = get_object_or_404(Content, id=content_id)
    content.increment_views()
    return content


@router.post("/{content_id}/increment-likes", response=ContentOut)
def increment_likes(request, content_id: int):
    """Increment like count for content."""
    content = get_object_or_404(Content, id=content_id)
    content.increment_likes()
    return content


@router.post("/{content_id}/increment-shares", response=ContentOut)
def increment_shares(request, content_id: int):
    """Increment share count for content."""
    content = get_object_or_404(Content, id=content_id)
    content.increment_shares()
    return content


@router.post("/{content_id}/increment-comments", response=ContentOut)
def increment_comments(request, content_id: int):
    """Increment comment count for content."""
    content = get_object_or_404(Content, id=content_id)
    content.increment_comments()
    return content


@router.get("/scheduled/upcoming", response=List[ContentOut])
@paginate(LimitOffsetPagination, page_size=10)
def get_upcoming_scheduled_content(request):
    """Get upcoming scheduled content."""
    from django.utils import timezone
    contents = Content.objects.filter(
        status='scheduled',
        scheduled_date__gte=timezone.now()
    ).order_by('scheduled_date')
    return contents
