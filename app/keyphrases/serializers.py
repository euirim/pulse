from rest_framework import serializers

from .models import Keyphrase

class KeyphraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyphrase
        fields = ('name',)