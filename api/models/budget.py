from django.db import models


class Budget(models.Model):
    class PaymentMethod(models.TextChoices):
        TRANSFER = "transfer", "Transfer"
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        CHEQUE = "cheque", "Cheque"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    invoice_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Invoice reference e.g. FJ9387HDS"
    )

    # we should get the client id and name from the project
    project_id = models.CharField(
        max_length=255,
        help_text="project"
    )

    budget_date = models.DateField()

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text="Budget amount"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-budget_date"]
        indexes = [
            models.Index(fields=["invoice_id"]),
            models.Index(fields=["project_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.invoice_id} - {self.project_id}"

    @property
    def amount_display(self):
        return f"{self.amount:,.2f}"
