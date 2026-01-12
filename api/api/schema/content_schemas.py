from ninja import Schema
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ContentIn(Schema):
    title: str
    content_type: str = "blog_post"
    status: str = "draft"
    platform: str
    body: str = ""
    excerpt: str = ""
    featured_image: Optional[str] = None
    views: int = 0
    likes: int = 0
    shares: int = 0
    comments: int = 0
    author_id: Optional[str] = None
    published_date: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None
    slug: str = ""
    external_url: str = ""
    meta_description: str = ""
    keywords: str = ""
    tags: str = ""
    category: str = ""
    is_featured: bool = False
    allow_comments: bool = True


class ContentUpdate(Schema):
    title: Optional[str] = None
    content_type: Optional[str] = None
    status: Optional[str] = None
    platform: Optional[str] = None
    body: Optional[str] = None
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    shares: Optional[int] = None
    comments: Optional[int] = None
    author_id: Optional[str] = None
    published_date: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None
    slug: Optional[str] = None
    external_url: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    is_featured: Optional[bool] = None
    allow_comments: Optional[bool] = None


class ContentOut(Schema):
    id: int
    title: str
    content_type: str
    status: str
    platform: str
    body: str
    excerpt: str
    featured_image: Optional[str]
    views: int
    likes: int
    shares: int
    comments: int
    author_id: Optional[str]
    published_date: Optional[datetime]
    scheduled_date: Optional[datetime]
    slug: str
    external_url: str
    meta_description: str
    keywords: str
    tags: str
    category: str
    is_featured: bool
    allow_comments: bool
    engagement_rate: float
    total_engagement: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ContentListOut(Schema):
    count: int
    results: List[ContentOut]
