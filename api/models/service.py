from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from api.utils.validators import validate_client_id, validate_user_id, validate_employee_id


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services')
    description = models.TextField()
    base_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    delivery_time = models.CharField(max_length=100, help_text="e.g., '3-5 weeks'")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from main auth service")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def clean(self):
        """Validate cross-service references before saving."""
        super().clean()
        errors = {}

        # Validate created_by (user_id)
        if self.created_by:
            try:
                validate_user_id(self.created_by)
            except ValidationError as e:
                errors['created_by'] = e.message

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to ensure validation happens."""
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)


class ServiceLead(models.Model):
    """
    Lead tracking - references clients from main backend via client_id.
    """
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('contacted', 'Contacted'),
        ('proposal_sent', 'Proposal Sent'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    # Reference to main backend Client via ID
    client_id = models.CharField(max_length=100, db_index=True, default='', help_text="Client ID from main auth service")
    client_name = models.CharField(max_length=255, default='', help_text="Cached client name for display")
    client_email = models.EmailField(blank=True, default='', help_text="Cached client email for display")

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='leads')
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from main auth service")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.client_name} - {self.service.name if self.service else 'No Service'}"

    def clean(self):
        """Validate cross-service references before saving."""
        super().clean()
        errors = {}

        # Validate client_id
        if self.client_id:
            try:
                client_info = validate_client_id(self.client_id)
                # Update cached fields
                if client_info:
                    self.client_name = client_info.get('client_name', self.client_name)
                    self.client_email = client_info.get('email', self.client_email)
            except ValidationError as e:
                errors['client_id'] = e.message

        # Validate created_by (user_id)
        if self.created_by:
            try:
                validate_user_id(self.created_by)
            except ValidationError as e:
                errors['created_by'] = e.message

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to ensure validation happens."""
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)


class Quote(models.Model):
    QUOTE_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    quote_number = models.CharField(max_length=50, unique=True, editable=False)

    # Reference to main backend Client via ID
    client_id = models.CharField(max_length=100, db_index=True, default='', help_text="Client ID from main auth service")
    client_name = models.CharField(max_length=255, default='', help_text="Cached client name for display")
    client_email = models.EmailField(blank=True, default='', help_text="Cached client email for display")

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='quotes')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from main auth service")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client_id']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        """Validate cross-service references before saving."""
        super().clean()
        errors = {}

        # Validate client_id
        if self.client_id:
            try:
                client_info = validate_client_id(self.client_id)
                # Update cached fields
                if client_info:
                    self.client_name = client_info.get('client_name', self.client_name)
                    self.client_email = client_info.get('email', self.client_email)
            except ValidationError as e:
                errors['client_id'] = e.message

        # Validate created_by (user_id)
        if self.created_by:
            try:
                validate_user_id(self.created_by)
            except ValidationError as e:
                errors['created_by'] = e.message

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Validate unless explicitly skipped
        if not kwargs.pop('skip_validation', False):
            self.full_clean()

        # Auto-generate quote_number
        if not self.quote_number:
            self.quote_number = f"QTE-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quote_number} - {self.client_name}"


class ServiceOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    order_number = models.CharField(max_length=50, unique=True, editable=False)

    # Reference to main backend Client via ID
    client_id = models.CharField(max_length=100, db_index=True, default='', help_text="Client ID from main auth service")
    client_name = models.CharField(max_length=255, default='', help_text="Cached client name for display")
    client_email = models.EmailField(blank=True, default='', help_text="Cached client email for display")

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orders')
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from main auth service")
    assigned_to = models.CharField(max_length=100, blank=True, help_text="Employee ID from main auth service")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['client_id']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),
        ]

    def clean(self):
        """Validate cross-service references before saving."""
        super().clean()
        errors = {}

        # Validate client_id
        if self.client_id:
            try:
                client_info = validate_client_id(self.client_id)
                # Update cached fields
                if client_info:
                    self.client_name = client_info.get('client_name', self.client_name)
                    self.client_email = client_info.get('email', self.client_email)
            except ValidationError as e:
                errors['client_id'] = e.message

        # Validate created_by (user_id)
        if self.created_by:
            try:
                validate_user_id(self.created_by)
            except ValidationError as e:
                errors['created_by'] = e.message

        # Validate assigned_to (employee_id) - optional field
        if self.assigned_to:
            try:
                validate_employee_id(self.assigned_to)
            except ValidationError as e:
                errors['assigned_to'] = e.message

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Validate unless explicitly skipped
        if not kwargs.pop('skip_validation', False):
            self.full_clean()

        # Auto-generate order_number
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.client_name}"
