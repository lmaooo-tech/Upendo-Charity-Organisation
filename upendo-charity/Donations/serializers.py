from rest_framework import serializers
from .models import Donation


class DonationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Donation model.
    
    Validates donation input and transforms data for API responses.
    """
    
    class Meta:
        model = Donation
        fields = [
            'id',
            'donor_name',
            'donor_email',
            'amount',
            'transaction_reference',
            'message',
            'timestamp'
        ]
        read_only_fields = ['id', 'transaction_reference', 'timestamp']
    
    def validate_amount(self, value):
        """Ensure amount is within valid range."""
        if value < 0.01:
            raise serializers.ValidationError("Amount must be at least 0.01")
        if value > 999999.99:
            raise serializers.ValidationError("Amount cannot exceed 999,999.99")
        return value
    
    def validate_message(self, value):
        """Ensure message doesn't exceed max length."""
        if value and len(value) > 500:
            raise serializers.ValidationError("Message cannot exceed 500 characters")
        return value


class DonationStatsSerializer(serializers.Serializer):
    """
    Serializer for donation statistics.
    
    Returns aggregated statistics about all donations.
    """
    total_amount_raised = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_donations = serializers.IntegerField()
    unique_donors = serializers.IntegerField()
    average_donation = serializers.DecimalField(max_digits=15, decimal_places=2)
