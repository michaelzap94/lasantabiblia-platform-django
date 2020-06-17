from rest_framework import serializers
from .models import Label, Verses_Marked, Verses_Learned # we need to serialize the model data

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label # name of model
        fields = ('id', '_id', 'name', 'color', 'permanent') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

class VersesMarkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verses_Marked # name of model
        fields = ('id', '_id', 'name', 'color', 'permanent') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

class VersesLearnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verses_Learned # name of model
        fields = ('id', '_id', 'name', 'color', 'permanent') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

