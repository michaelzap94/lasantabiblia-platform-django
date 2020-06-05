from rest_framework import serializers
from .models import Course, Label # we need to serialize the model data

#class CourseSerializer(serializers.ModelSerializer):
# you can use the HyperlinkedModelSerializer SO a 'url' FIELD can be added to the fields property for us.
#the url will be the link to the specific model data
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Course object"""
    class Meta:
        model = Course # name of model
        fields = ('id', 'url', 'name', 'language', 'price') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

class LabelSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Course object"""
    class Meta:
        model = Label # name of model
        fields = ('id', '_id', 'name', 'color', 'permanent') #fields we want to serialize( convert to/from JSON)
        read_only_Fields = ('id',) #fields that we want to protect

