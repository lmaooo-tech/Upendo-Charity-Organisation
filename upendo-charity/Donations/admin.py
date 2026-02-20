from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Admin interface for monitoring donations.
    
    Features:
    - List view with key donation information
    - Filtering by date and amount range
    - Search by transaction reference or donor email
    - Read-only fields for audit trail protection
    """
    
    list_display = [
        'transaction_reference',
        'donor_name',
        'donor_email',
        'amount',
        'timestamp'
    ]
    
    list_filter = [
        'timestamp',
        'amount',
    ]
    
    search_fields = [
        'transaction_reference',
        'donor_email',
        'donor_name'
    ]
    
    readonly_fields = [
        'transaction_reference',
        'id',
        'timestamp'
    ]
    
    fieldsets = (
        ('Donation Reference', {
            'fields': ('id', 'transaction_reference', 'timestamp')
        }),
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email')
        }),
        ('Donation Details', {
            'fields': ('amount', 'message')
        }),
    )
    
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Disable manual donation creation in admin."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of donation records (audit trail)."""
        return False
