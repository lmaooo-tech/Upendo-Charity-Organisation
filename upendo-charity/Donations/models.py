from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import datetime


class Donation(models.Model):
    """
    Model to store donation transactions.
    
    Fields:
    - id: Auto-generated primary key
    - donor_name: Optional donor name (max 100 characters)
    - donor_email: Optional donor email (max 254 characters)
    - amount: Donation amount in decimal (0.01 to 999,999.99)
    - transaction_reference: Unique auto-generated transaction ID
    - message: Optional donation message (max 500 characters)
    - timestamp: Auto-generated timestamp when donation is created
    """
    
    donor_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Name of the donor (optional)"
    )
    
    donor_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address of the donor (optional)"
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(999999.99)
        ],
        help_text="Donation amount in currency (0.01 to 999,999.99)"
    )
    
    transaction_reference = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        db_index=True,
        help_text="Unique transaction reference (auto-generated)"
    )
    
    message = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional message from the donor (max 500 characters)"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when donation was created"
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['transaction_reference']),
            models.Index(fields=['-timestamp']),
        ]
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
    
    def __str__(self):
        return f"Donation {self.transaction_reference} - ${self.amount}"
    
    def save(self, *args, **kwargs):
        """Auto-generate transaction reference if not provided."""
        if not self.transaction_reference:
            # Format: TXN-YYYYMMDD-XXXXXX
            date_str = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.transaction_reference = f"TXN-{date_str}-{unique_id}"
        super().save(*args, **kwargs)
