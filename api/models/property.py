from django.db import models


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('land', 'Land'),
    ]

    CATEGORY_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('reserved', 'Reserved'),
        ('pending', 'Pending'),
        ('off_market', 'Off Market'),
    ]

    name = models.CharField(max_length=255, verbose_name="Property Name")
    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name="Property Type"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Category"
    )

    location = models.TextField(verbose_name="Location/Address")

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Price (₦)"
    )
    size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Size (sqm)"
    )

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    parking_spaces = models.PositiveIntegerField(default=0)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="Status"
    )
    client_id = models.CharField(
        max_length=255,
        verbose_name="Owner",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
