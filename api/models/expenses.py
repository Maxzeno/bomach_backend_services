from django.db import models

class Expense(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    CATEGORY_CHOICES = [
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('accommodation', 'Accommodation'),
        ('equipment', 'Equipment'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    user_id = models.CharField(max_length=255)

    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='other'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"