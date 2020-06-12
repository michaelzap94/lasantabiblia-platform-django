from rest_framework import serializers
from .models import Resource # we need to serialize the model data

class ResourceSerializerWithLink(serializers.HyperlinkedModelSerializer):
    """Serializer for Resource object"""
    class Meta:
        model = Resource # name of model
        fields = ('id', 'url', 'name', 'resource_type', 'language', 'description', 'version', 'filename', 'size', 'resource') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect
        
class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource object"""
    class Meta:
        model = Resource # name of model
        fields = ('id', 'name', 'resource_type', 'language', 'description', 'version', 'filename', 'size', 'resource') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

