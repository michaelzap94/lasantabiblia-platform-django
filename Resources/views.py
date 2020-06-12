from django.shortcuts import render
from rest_framework import viewsets #sets of pages that the rest_framework will create for us
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions

from .serializer import ResourceSerializer, ResourceSerializerWithLink
from .models import Resource

SUPPORTED_ACCOUNT_TYPES = ['google']
#===============================================================
#permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser|IsOwner] # only admin or owner to continue
#===============================================================
# class IsOwnerOrAdmin(permissions.BasePermission):
#     """
#     Custom permission to allow admin or owner to edit
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.owner == request.user or request.user.is_admin
#===============================================================
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.owner == request.user
#permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#===============================================================
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return request.user.is_admin

#permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#===============================================================

class ResourcesByTypeView(APIView):
    # specified in settings
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication)
    #permission_classes = (permissions.IsAuthenticated,)
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, resource_type):
        allResources = Resource.objects.filter(resource_type=resource_type)
        serialized = ResourceSerializer(allResources, many=True)
        return Response(serialized.data)

class ResourcesByLangView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, language):
        allResources = Resource.objects.filter(language=language)
        serialized = ResourceSerializer(allResources, many=True)
        return Response(serialized.data)

class ResourcesExtraView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        allResources = Resource.objects.exclude(resource_type="bibles")
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
    #permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Resource.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = ResourceSerializerWithLink # Specify which serializer_class to use (show) when this view is accessed/served
