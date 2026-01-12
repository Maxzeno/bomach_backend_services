from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from api.models.service import Service, ServiceLead, ServiceOrder
from api.utils.validators import validate_client_id, validate_user_id, validate_employee_id


class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)

    # Reference to main backend Client via ID
    client_id = models.CharField(max_length=100, db_index=True, default='', help_text="Client ID from main auth service")
    client_name = models.CharField(max_length=255, default='', help_text="Cached client name for display")
    client_email = models.EmailField(blank=True, default='', help_text="Cached client email for display")

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='invoices')
    order = models.ForeignKey(ServiceOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    lead = models.ForeignKey(ServiceLead, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    issue_date = models.DateField()
    due_date = models.DateField()

    subtotal = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('7.50'), validators=[MinValueValidator(Decimal('0.00'))])
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])

    status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, default='draft')
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

        # Auto-generate invoice_number
        if not self.invoice_number:
            from datetime import datetime
            year = datetime.now().year
            month = datetime.now().month
            random_id = uuid.uuid4().hex[:8].upper()
            self.invoice_number = f"SRV-{year}-{month:02d}-{random_id}"

        # Calculate tax and total
        self.tax_amount = (self.subtotal * self.tax_rate) / Decimal('100')
        self.total_amount = self.subtotal + self.tax_amount

        super().save(*args, **kwargs)

    @property
    def balance(self):
        return self.total_amount - self.amount_paid

    @property
    def payment_progress(self):
        if self.total_amount == 0:
            return 0
        return (self.amount_paid / self.total_amount) * 100

    def __str__(self):
        return f"{self.invoice_number} - {self.client_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('card', 'Card'),
        ('mobile_money', 'Mobile Money'),
        ('other', 'Other'),
    ]

    payment_reference = models.CharField(max_length=100, unique=True, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateField()
    transaction_reference = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from main auth service")

    class Meta:
        ordering = ['-payment_date']

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
        from django.db import transaction

        # Validate unless explicitly skipped
        if not kwargs.pop('skip_validation', False):
            self.full_clean()

        # Auto-generate payment_reference
        if not self.payment_reference:
            self.payment_reference = f"PAY-{uuid.uuid4().hex[:12].upper()}"

        # Use atomic transaction with select_for_update to prevent race conditions
        with transaction.atomic():
            super().save(*args, **kwargs)

            # Lock the invoice row for update to prevent concurrent modifications
            invoice = Invoice.objects.select_for_update().get(pk=self.invoice_id)

            # Update invoice amount_paid with atomic calculation
            total_paid = invoice.payments.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
            invoice.amount_paid = total_paid

            # Update invoice status based on payment
            if total_paid >= invoice.total_amount:
                invoice.status = 'paid'
            elif total_paid > 0:
                invoice.status = 'partially_paid'

            invoice.save(update_fields=['amount_paid', 'status', 'updated_at'])

    def __str__(self):
        return f"{self.payment_reference} - {self.invoice.invoice_number}"
