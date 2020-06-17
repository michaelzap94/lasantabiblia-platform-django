from rest_framework import serializers
from .models import SyncUp # we need to serialize the model data

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

class SyncUpSerializer(serializers.ModelSerializer):
    updated_epoch  = UnixEpochDateField(source='updated')
    class Meta:
        model = SyncUp # name of model
        fields = ('id', 'user', 'version', 'last_device', 'updated', 'updated_epoch') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id','user','updated','updated_epoch',) #fields that we want to protect

