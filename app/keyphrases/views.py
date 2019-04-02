from rest_framework.response import Response

from rest_framework.viewsets import ViewSet

from .models import Keyphrase
from .serializers import KeyphraseSerializer

# Create your views here.
class KeyphraseViewSet(ViewSet):
    """
    Viewset for listing keyphrases for display.
    """
    def list(stself, request):
        keyphrases = Keyphrase.objects.filter(display=True, active=True)
        keyphrases = [k.name for k in keyphrases]
        return Response(keyphrases)