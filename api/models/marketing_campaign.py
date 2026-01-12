from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class MarketingCampaign(models.Model):
    """
    Model to track marketing campaign performance
    """
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('draft', 'Draft'),
    ]
    
    CHANNEL_CHOICES = [
        ('social_media', 'Social Media'),
        ('email', 'Email'),
        ('search', 'Search'),
        ('display', 'Display'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    # Campaign Basic Information
    name = models.CharField(
        max_length=255,
        verbose_name=_("Campaign Name"),
        help_text=_("Name of the marketing campaign")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("Brief description of the campaign target audience or purpose")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("Status")
    )
    
    channel = models.CharField(
        max_length=50,
        choices=CHANNEL_CHOICES,
        verbose_name=_("Marketing Channel")
    )
    
    # Performance Metrics
    impressions = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Impressions"),
        help_text=_("Total number of times the campaign was displayed")
    )
    
    ctr = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("CTR (%)"),
        help_text=_("Click-through rate as a percentage")
    )
    
    roi = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name=_("ROI (%)"),
        help_text=_("Return on Investment as a percentage")
    )
    
    # Progress/Completion
    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Progress (%)"),
        help_text=_("Campaign completion percentage")
    )
    
    # Budget Information
    budget_allocated = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Budget Allocated"),
        help_text=_("Total budget allocated for the campaign")
    )
    
    budget_spent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Budget Spent"),
        help_text=_("Amount spent so far")
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Start Date")
    )
    
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("End Date")
    )
    
    class Meta:
        verbose_name = _("Marketing Campaign")
        verbose_name_plural = _("Marketing Campaigns")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['channel']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    @property
    def budget_remaining(self):
        """Calculate remaining budget"""
        return self.budget_allocated - self.budget_spent
    
    @property
    def budget_utilization_percentage(self):
        """Calculate budget utilization percentage"""
        if self.budget_allocated > 0:
            return (self.budget_spent / self.budget_allocated) * 100
        return 0
    
    @property
    def is_over_budget(self):
        """Check if campaign is over budget"""
        return self.budget_spent > self.budget_allocated
    
    @property
    def clicks(self):
        """Calculate total clicks based on impressions and CTR"""
        if self.impressions > 0 and self.ctr > 0:
            return int((self.ctr / 100) * self.impressions)
        return 0
    
    def save(self, *args, **kwargs):
        """Override save to calculate progress based on budget spent"""
        if self.budget_allocated > 0:
            self.progress_percentage = (self.budget_spent / self.budget_allocated) * 100
            # Cap at 100%
            if self.progress_percentage > 100:
                self.progress_percentage = 100
        super().save(*args, **kwargs)
