from django.shortcuts import render
from rest_framework import viewsets #sets of pages that the rest_framework will create for us
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import ResourceSerializer
from .models import Resource

SUPPORTED_ACCOUNT_TYPES = ['google']

class ResourcesByTypeView(APIView):
    # specified in settings
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, resource_type):
        allResources = Resource.objects.filter(resource_type=resource_type)
        serialized = ResourceSerializer(allResources, many=True)
        return Response(serialized.data)

class ResourcesByLangView(APIView):
    # specified in settings
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, language):
        allResources = Resource.objects.filter(language=language)
        serialized = ResourceSerializer(allResources, many=True)
        return Response(serialized.data)

# class ResourcesAllView(APIView):
#     # specified in settings
#     # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication)
#     #permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         allResources = Resource.objects.all()
#         serialized = ResourceSerializer(allResources, many=True)
#         return Response(serialized.data)

# VIEWSETS HANDLE API requests and Responses only, if you need to handle HTTP req/res use APIView
class ResourcesAllView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = (IsAuthenticated,)
    queryset = Resource.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = ResourceSerializer # Specify which serializer_class to use (show) when this view is accessed/served
