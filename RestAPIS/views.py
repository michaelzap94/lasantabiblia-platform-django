from django.shortcuts import render
from rest_framework import viewsets, permissions #sets of pages that the rest_framework will create for us
from .models import Label, Verses_Marked, Verses_Learned
from .serializer import LabelSerializer, VersesMarkedSerializer, VersesMarkedSerializer
    
class LabelView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = [permissions.DjangoModelPermissions]

    queryset = Label.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = LabelSerializer # Specify which serializer_class to use (show) when this view is accessed/served
    
