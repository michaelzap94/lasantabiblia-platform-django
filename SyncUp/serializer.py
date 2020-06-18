from rest_framework import serializers
from .models import SyncUp # we need to serialize the model data
from RestAPIS.models import Label, Verses_Marked, Verses_Learned
from RestAPIS.serializer import LabelSerializer, VersesMarkedSerializer, VersesLearnedSerializer
from django.db import transaction
class UnixEpochDateField(serializers.DateTimeField):
    def to_representation(self, value):
        """ Return epoch time for a datetime object or ``None``"""
        import time
        try:
            return int(time.mktime(value.timetuple()))
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        import datetime
        return datetime.datetime.fromtimestamp(int(value))

class SyncUpModelSerializer(serializers.ModelSerializer):
    updated_epoch  = UnixEpochDateField(source='updated')
    class Meta:
        model = SyncUp # name of model
        fields = ('id', 'user', 'version', 'last_device', 'updated', 'updated_epoch') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id','user','updated','updated_epoch',) #fields that we want to protect
#=============================================================================================================
class OverrideLabelsSerializer(serializers.Serializer):
    labels = LabelSerializer(required=False, many=True)
    verses_marked = VersesMarkedSerializer(required=False, many=True)
    verses_learned = VersesLearnedSerializer(required=False, many=True)
    
    @transaction.atomic
    def create(self, validated_data):
        # logic to update labels
        labels_list_of_objects = validated_data.pop('labels', None)
        #label_group = Label.objects.create(**validated_data)
        for label in labels_list_of_objects:
            Label.objects.create(**label)
        # logic to update verses_marked
        verses_marked_list_of_objects = validated_data.pop('verses_marked', None)
        #verses_marked_group = Verses_Marked.objects.create(**validated_data)
        for verse_marked in verses_marked_list_of_objects:
            Verses_Marked.objects.create(**verse_marked)

        # logic to update verses_learned
        verses_learned_list_of_objects = validated_data.pop('verses_learned', None)
        #verses_learned_group = Verses_Learned.objects.create(**validated_data)
        for verse_learned in verses_learned_list_of_objects:
            Verses_Learned.objects.create(**verse_learned)

        return True

    # def update(self, validated_data):
    #     labels_list_of_objects = validated_data.pop('labels', None)
    #     # logic to update labels
    #     verses_marked_list_of_objects = validated_data.pop('verses_marked', None)
    #     # logic to update verses_marked
    #     verses_learned_list_of_objects = validated_data.pop('verses_learned', None)
    #     # logic to update verses_learned
    #     return super().update(validated_data)
#=============================================================================================================


