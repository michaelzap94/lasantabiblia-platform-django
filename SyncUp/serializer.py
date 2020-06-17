from rest_framework import serializers
from .models import SyncUp # we need to serialize the model data
from RestAPIS.models import Label, Verses_Marked, Verses_Learned
from RestAPIS.serializer import LabelSerializer, VersesMarkedSerializer, VersesLearnedSerializer

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
    # class Meta:
    #     fields = ('labels', 'verses_marked', 'verses_learned') #fields we want to serialize( convert to/from JSON)
#=============================================================================================================


