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
from RestAPIS.models import Label, Verses_Marked, Verses_Learned, Notes
import json

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
                data['error'] = "Version was not sent by the client."
                return Response(data)
            elif server_version == None:
                data['status'] = "error"
                data['error'] = "Version is not present in the server."
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

class ServerSyncUpDBProcessView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            data = {}
            try:
                labels = Label.objects.filter(user=user.id)
                verses_marked = Verses_Marked.objects.filter(user=user.id)
                verses_learned = Verses_Learned.objects.filter(user=user.id)
                notes = Notes.objects.filter(user=user.id)
            except Exception as e:
                data["status"] = "error"
                data["error"] = str(e)
                return Response(data)

            dataToSync = {
                "labels": labels,
                "verses_marked": verses_marked,
                "verses_learned": verses_learned,
                "notes": notes
            }

            serialized = OverrideLabelsSerializer(dataToSync, many=False)

            try:
                sync_up_object = SyncUp.objects.get(user=user.id)
                data = serialized.data
                data['status'] = 'success'
                data['version'] = sync_up_object.version
                # data['result'] = serialized.data
            except Exception as e:
                data["status"] = "error"
                data["error"] = str(e)

            # try:
            #     sync_up_object = SyncUp.objects.get(user=user.id)
            # except Exception as e:
            #     data["status"] = "error"
            #     data["error"] = str(e)
            #     return Response(data)
            # data['status'] = 'success'
            # data['version'] = sync_up_object.version
            # data['result'] = dataToSync

            return Response(data)
        raise PermissionDenied()

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            data = {}
            client_version = request.data.get('version', None)
            client_state = request.data.get('state', None)
            if client_version == None:
                data['status'] = "error"
                data['error'] = "Version was not sent by the client."
                return Response(data)
            if client_state == None:
                data['status'] = "error"
                data['error'] = "State was not sent by the client."
                return Response(data)

            labels = request.data.get('labels', None)
            verses_marked = request.data.get('verses_marked', None)
            verses_learned = request.data.get('verses_learned', None)
            notes = request.data.get('notes', None)
            dataToSync = {
                "userId": user.id,
                "labels": labels,
                "verses_marked": verses_marked,
                "verses_learned": verses_learned,
                "notes": notes,
            }

            serialized = OverrideLabelsSerializer(data=dataToSync, many=False)

            if serialized.is_valid(): #and client_version != None and client_state!=None handled before
                try:
                    success = serialized.save()#FIRST DELETE ALL THEN insert the data
                except Exception as e:
                    data["status"] = "error"
                    data["error"] = str(e)
                    return Response(data)
                if success:
                    new_version = client_version + 1 if client_state == 0 else client_version
                    #Update SyncUp version for this user
                    try: 
                        sync_up = SyncUp.objects.get(user=user.id)
                        sync_up.version = new_version
                        sync_up.save()
                        updateVersionResult = True
                    except Exception:
                        updateVersionResult = False

                    if updateVersionResult:
                        data['status'] = 'success'
                        data['version'] = new_version
                    else:
                        data['status'] = 'error'
                        data['error'] = 'Data was saved in the Server but Version was not updated'
                else:
                    data['status'] = 'error'
                    data['error'] = 'Data could not be saved in Server'
            else:
                data['status'] = 'error'
                data['error'] = json.dumps(serialized.errors)
            return Response(data)
        raise PermissionDenied()



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
                
