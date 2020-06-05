from django.shortcuts import render
from rest_framework import viewsets, permissions #sets of pages that the rest_framework will create for us
from .models import Course, Label
from .serializer import CourseSerializer, LabelSerializer

class CourseView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = [permissions.DjangoModelPermissions]

    queryset = Course.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = CourseSerializer # Specify which serializer_class to use (show) when this view is accessed/served
    
class LabelView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = [permissions.DjangoModelPermissions]

    queryset = Label.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = LabelSerializer # Specify which serializer_class to use (show) when this view is accessed/served
    
