from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Content(models.Model):
    """
    Model for managing marketing content (blog posts, social media posts, etc.)
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('blog_post', 'Blog Post'),
        ('social_media', 'Social Media'),
        ('video', 'Video'),
        ('infographic', 'Infographic'),
        ('newsletter', 'Newsletter'),
        ('article', 'Article'),
    ]
    
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('website', 'Website'),
        ('medium', 'Medium'),
        ('youtube', 'YouTube'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=500,
        verbose_name=_("Title"),
        help_text=_("Content title or headline")
    )
    
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_TYPE_CHOICES,
        default='blog_post',
        verbose_name=_("Content Type")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("Status")
    )
    
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        verbose_name=_("Platform"),
        help_text=_("Platform where content is published")
    )
    
    # Content Details
    body = models.TextField(
        blank=True,
        verbose_name=_("Content Body"),
        help_text=_("Main content/text")
    )
    
    excerpt = models.TextField(
        blank=True,
        max_length=500,
        verbose_name=_("Excerpt"),
        help_text=_("Short description or summary")
    )
    
    featured_image = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Featured Image")
    )
    
    # Engagement Metrics
    views = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Views"),
        help_text=_("Number of times content was viewed")
    )
    
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Likes"),
        help_text=_("Number of likes/reactions")
    )
    
    shares = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Shares"),
        help_text=_("Number of times content was shared")
    )
    
    comments = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Comments"),
        help_text=_("Number of comments")
    )
    
    # Author and Assignment
    author_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        related_name='authored_content',
        verbose_name=_("Author")
    )

    # Publishing Information
    published_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Published Date"),
        help_text=_("Date and time when content was published")
    )
    
    scheduled_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Scheduled Date"),
        help_text=_("Date and time to automatically publish")
    )
    
    # SEO and URLs
    slug = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
        verbose_name=_("URL Slug")
    )
    
    external_url = models.URLField(
        blank=True,
        verbose_name=_("External URL"),
        help_text=_("URL where content is published externally")
    )
    
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Meta Description")
    )
    
    keywords = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Keywords"),
        help_text=_("Comma-separated keywords for SEO")
    )
    
    # Tags and Categories
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("Comma-separated tags")
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Category")
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    # Additional Flags
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured"),
        help_text=_("Mark as featured content")
    )
    
    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_("Allow Comments")
    )
    
    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Content")
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_date']),
            models.Index(fields=['content_type', 'platform']),
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    @property
    def engagement_rate(self):
        """Calculate engagement rate based on views"""
        if self.views > 0:
            total_engagement = self.likes + self.shares + self.comments
            return (total_engagement / self.views) * 100
        return 0
    
    @property
    def total_engagement(self):
        """Calculate total engagement"""
        return self.likes + self.shares + self.comments
    
    @property
    def is_published(self):
        """Check if content is published"""
        return self.status == 'published'
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def increment_likes(self):
        """Increment like count"""
        self.likes += 1
        self.save(update_fields=['likes'])
    
    def increment_shares(self):
        """Increment share count"""
        self.shares += 1
        self.save(update_fields=['shares'])
    
    def increment_comments(self):
        """Increment comment count"""
        self.comments += 1
        self.save(update_fields=['comments'])