from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions #sets of pages that the rest_framework will create for us
from rest_framework.authtoken.models import Token
# Used for create-only endpoints. Provides a post method handler.
from rest_framework.generics import CreateAPIView
# Creating tokens manually using function
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import get_user_model  # If used custom user model

from RestAPIS.models import Label
from RestAPIS.serializer import LabelSerializer
from .serializers import RegistrationSerializer  # , UserSerializer
from Account.models import Account

# Register
# Response: {
#     "response": "successfully registered new user.",
#     "email": "test1223@tabian.ca",
#     "username": "test1232",
#     "pk": 1,
#     "token": "c2f020e5d8a88d888d2da67e08098f5113f753a5"
# }
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['firstname'] = account.firstname
			data['lastname'] = account.lastname
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

# Register
# Response: {
#     "response": "successfully registered new user.",
#     "email": "test1223@tabian.ca",
#     "username": "test1232",
#     "pk": 1,
#     "jwt": {
#     		"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eX...",
#     		"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tll90eXBl..."
# 		}
# }
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view_jwt(request):
	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)

		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['firstname'] = account.firstname
			data['lastname'] = account.lastname

			data['jwt'] = get_tokens_for_user(account)
		else:
			data = serializer.errors
		return Response(data)

def get_tokens_for_user(account):
    refresh = RefreshToken.for_user(account)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email
# ============================================================================================================================
class RegisterUserOnlyView(CreateAPIView):
    # Otherwise anonymous/new users won't be able to register
    permission_classes = [ permissions.AllowAny ]

    model = get_user_model() # this is the model (dataset), so we need to pull out the data
    serializer_class = RegistrationSerializer # Specify which serializer_class to use (show) when this view is accessed/served
# ============================================================================================================================
class TestAllLabels(APIView):
    # specified in settings
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # GET THE SQL DB DATA
        # this is the model (dataset), so we need to pull out the data
        allLabels = Label.objects.all()
        # Serialize the DB DATA INTO JSON
        serialized = LabelSerializer(allLabels, many=True)
        # Return using a normal HTTP response JSON object USE IT WITH REST FRAMEWORK
        return Response(serialized.data)

# VIEWSETS HANDLE API requests and Responses only, if you need to handle HTTP req/res use APIView
# class LabelView(viewsets.ModelViewSet): 
#     #YOU WOULD GET: {"detail": "Authentication credentials were not provided."} IF not LOGGED IN
#     permission_classes = [permissions.DjangoModelPermissions] or use the imported (IsAuthenticated,) in settings
#     queryset = Label.objects.all() # this is the model (dataset), so we need to pull out the data
#     serializer_class = LabelSerializer # Specify which serializer_class to use (show) when this view is accessed/served
