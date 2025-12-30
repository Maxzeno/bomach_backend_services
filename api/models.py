from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


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
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Client(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    project_description = models.TextField(blank=True, help_text="Project or location description")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ServiceLead(models.Model):
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('contacted', 'Contacted'),
        ('proposal_sent', 'Proposal Sent'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='leads')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='leads')
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client.name} - {self.service.name if self.service else 'No Service'}"


class Quote(models.Model):
    QUOTE_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    quote_number = models.CharField(max_length=50, unique=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='quotes')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='quotes')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.quote_number:
            self.quote_number = f"QTE-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quote_number} - {self.client.name}"


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orders')
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, help_text="User ID from user service")
    assigned_to = models.CharField(max_length=100, blank=True, help_text="Employee ID from user service")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.client.name}"


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
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
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
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
        return f"{self.invoice_number} - {self.client.name}"


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
    created_by = models.CharField(max_length=100, help_text="User ID from user service")

    class Meta:
        ordering = ['-payment_date']

    def save(self, *args, **kwargs):
        if not self.payment_reference:
            self.payment_reference = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

        # Update invoice amount_paid
        total_paid = self.invoice.payments.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        self.invoice.amount_paid = total_paid

        # Update invoice status based on payment
        if total_paid >= self.invoice.total_amount:
            self.invoice.status = 'paid'
        elif total_paid > 0:
            self.invoice.status = 'partially_paid'

        self.invoice.save()

    def __str__(self):
        return f"{self.payment_reference} - {self.invoice.invoice_number}"
