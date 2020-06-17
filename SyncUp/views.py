from django.shortcuts import render
from rest_framework import viewsets #sets of pages that the rest_framework will create for us
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.exceptions import PermissionDenied

# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions

from .serializer import SyncUpModelSerializer, OverrideLabelsSerializer
from .models import SyncUp
from utilities.my_atomic_viewsets import AtomicModelViewSet

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# VIEWSETS HANDLE API requests and Responses only, if you need to handle HTTP req/res use APIView
class SyncUpAllView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # only admin to continue
    queryset = SyncUp.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = SyncUpModelSerializer # Specify which serializer_class to use (show) when this view is accessed/served

#FIRST CHECK THE USER IS LOGGEDIN, THEN CHECK IF USER IS AUTHORIZED TO PERFORM THIS ACTION
# @permission_classes([permissions.IsAuthenticated, IsOwner])
class ServerDBVersionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    # GETS SERVER VERSION
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            syncup_data = SyncUp.objects.get(user=user.id)
            serialized = SyncUpModelSerializer(syncup_data, many=False)
            return Response(serialized.data)
        raise PermissionDenied()
    # CHECKS SERVER VERSION is same as CLIENT
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            data = {}
            syncup_data = SyncUp.objects.get(user=user.id)
            #serialized = SyncUpModelSerializer(syncup_data, many=True) #not needed
            client_version = request.data.get('version', None)
            server_version = syncup_data.version
            if client_version == None:
                data['status'] = "error"
                data['detail'] = "Version was not sent by the client."
                return Response(data)
            elif server_version == None:
                data['status'] = "error"
                data['detail'] = "Version is not present in the server."
                return Response(data)
            else:
                client_version = int(client_version)
                if client_version  == server_version:
                    data['status'] = "success"
                    data['result'] = True
                    return Response(data)
                else:
                    data['status'] = "success"
                    data['result'] = False
                    return Response(data)
            # return Response(serialized.data)
        raise PermissionDenied()

class ServerDBOverrideView(AtomicModelViewSet):
    pass

# class ServerDBOverrideView(AtomicModelViewSet):
#     permission_classes = [permissions.IsAuthenticated, IsOwner]
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     #search_fields = ('name','author')
#     def create(self, request, *args, **kwargs):
#         """
#         #checks if post request data is an array initializes serializer with many=True
#         else executes default CreateModelMixin.create function 
#         """
#         is_many = isinstance(request.data, list)
#         if not is_many:
#             return super(ServerDBOverrideView, self).create(request, *args, **kwargs)
#         else:
#             serializer = self.get_serializer(data=request.data, many=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class ServerDBSyncUpView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwner]
#     pass
                
