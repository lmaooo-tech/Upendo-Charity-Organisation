from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from decimal import Decimal

from .models import Donation
from .serializers import DonationSerializer, DonationStatsSerializer


@api_view(['POST'])
def donate(request):
    """
    Donation submission endpoint.
    
    POST /api/donations/donate/
    
    Accepts donation data and creates a new donation record.
    Returns 201 Created with the donation object including auto-generated
    transaction reference.
    
    Request body:
    {
        "amount": "150.50",
        "donor_name": "John Doe" (optional),
        "donor_email": "john@example.com" (optional),
        "message": "Supporting education" (optional)
    }
    """
    serializer = DonationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def stats(request):
    """
    Donation statistics endpoint.
    
    GET /api/donations/stats/
    
    Returns public fundraising statistics aggregated from all donations.
    No authentication required.
    
    Response:
    {
        "total_amount_raised": "5250.75",
        "total_donations": 25,
        "unique_donors": 18,
        "average_donation": "210.03"
    }
    """
    # Get all donations
    donations = Donation.objects.all()
    
    # Calculate statistics
    total_raised = donations.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_count = donations.count()
    unique_donors = donations.filter(donor_email__isnull=False).values('donor_email').distinct().count()
    average_donation = donations.aggregate(Avg('amount'))['amount__avg'] or Decimal('0.00')
    
    # Format average to 2 decimal places
    if average_donation:
        average_donation = Decimal(str(average_donation)).quantize(Decimal('0.01'))
    
    stats_data = {
        'total_amount_raised': total_raised,
        'total_donations': total_count,
        'unique_donors': unique_donors,
        'average_donation': average_donation
    }
    
    serializer = DonationStatsSerializer(stats_data)
    return Response(serializer.data, status=status.HTTP_200_OK)
