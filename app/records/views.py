import datetime

from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.viewsets import ViewSet

from .models import Record
from .serializers import RecordSerializer

# Create your views here.
class RecordViewSet(ViewSet):
    """
    Viewset for listing records.
    """
    def list(stself, request):
        base_time = timezone.now() - datetime.timedelta(days=1)
        records = Record.objects.filter(
            time_created__gte=base_time
        ).order_by('time_created')
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)