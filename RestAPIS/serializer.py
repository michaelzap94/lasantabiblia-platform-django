from rest_framework import serializers
from .models import Label, Verses_Marked, Verses_Learned, Notes # we need to serialize the model data

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label # name of model
        fields = ('id', 'user', '_id', 'name', 'color', 'permanent', 'state') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

class VersesMarkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verses_Marked # name of model
        fields = ('id', 'user', '_id', 'label_id', 'book_number', 'chapter', 'verseFrom', 'verseTo', 'label_name', 'label_color', 'label_permanent', 'note', 'date_created', 'date_updated', 'UUID', 'state')
        read_only_Fields = ('id',) #fields that we want to protect

class VersesLearnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verses_Learned # name of model
        fields = ('id', 'user', '_id', 'UUID', 'label_id', 'learned', 'priority', 'state') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes # name of model
        fields = ('id', 'user', '_id', 'label_id', 'title', 'content', 'date_created', 'date_updated', 'state')
        read_only_Fields = ('id',) #fields that we want to protect
        