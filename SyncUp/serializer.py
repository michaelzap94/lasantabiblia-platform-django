from rest_framework import serializers
from .models import SyncUp # we need to serialize the model data

class SyncUpSerializer(serializers.ModelSerializer):
    """Serializer for Resource object"""
    class Meta:
        model = SyncUp # name of model
        fields = ('id', 'user', 'version', 'last_device', 'updated') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id','user','updated',) #fields that we want to protect