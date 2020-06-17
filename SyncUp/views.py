from django.shortcuts import render
from rest_framework import viewsets #sets of pages that the rest_framework will create for us
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.exceptions import PermissionDenied

# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import permissions

from .serializer import SyncUpSerializer
from .models import SyncUp

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# VIEWSETS HANDLE API requests and Responses only, if you need to handle HTTP req/res use APIView
class SyncUpAllView(viewsets.ModelViewSet):
    #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # only admin to continue
    queryset = SyncUp.objects.all() # this is the model (dataset), so we need to pull out the data
    serializer_class = SyncUpSerializer # Specify which serializer_class to use (show) when this view is accessed/served

#FIRST CHECK THE USER IS LOGGEDIN, THEN CHECK IF USER IS AUTHORIZED TO PERFORM THIS ACTION
# @permission_classes([permissions.IsAuthenticated, IsOwner])
class CheckClientHasLatestVersionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    # Ensure a user sees only own SyncUp objects.
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            data = {}
            syncup_data = SyncUp.objects.get(user=user.id)
            #serialized = SyncUpSerializer(syncup_data, many=True) #not needed
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
                
