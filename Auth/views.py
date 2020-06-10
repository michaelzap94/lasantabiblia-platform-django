from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response  # Rest framework response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# sets of pages that the rest_framework will create for us
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
# Used for create-only endpoints. Provides a post method handler.
from rest_framework.generics import CreateAPIView
# Creating tokens manually using function
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from google.oauth2 import id_token
from google.auth.transport import requests

import json
import os

from django.contrib.auth import get_user_model  # If used custom user model

from RestAPIS.models import Label
from RestAPIS.serializer import LabelSerializer
from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer, TokenRegistrationSerializer
from Account.models import Account

SUPPORTED_ACCOUNT_TYPES = ['google']

# Register
# Response: {
#     "status": "success",
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
            data['error'] = 'That email is already in use.'
            data['status'] = 'error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['status'] = 'success'
            data['email'] = account.email
            data['account_type'] = account.account_type
            data['fullname'] = account.fullname
            data['firstname'] = account.firstname
            data['lastname'] = account.lastname
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data['status'] = 'error'
            data['error'] = json.dumps(serializer.errors)
        return Response(data)
# ============================================================================================================================
# Register
# Response: {
#           "status": "success"
#     		"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eX...",
#     		"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tll90eXBl..."
# 		}
# Url: https://<your-domain>/api/account/register


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view_jwt(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) != None:
            data['error'] = 'That email is already in use.'
            data['status'] = 'error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            #the JWT token will contain the data I need about the user
            data = get_tokens_with_data(account)
        else:
            data['status'] = 'error'
            data['error'] = json.dumps(serializer.errors)
        return Response(data)

def get_tokens_with_data(account):
	refresh = MyTokenObtainPairSerializer.get_token(account)
	return {
		'refresh': str(refresh),
		'access': str(refresh.access_token),
        'status': 'success'
	}

def get_tokens_for_user(account):
    refresh = RefreshToken.for_user(account)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def logout_view_jwt(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh', None)
        if refresh_token != None:
            data = blacklist_refresh_token(refresh_token)
            return Response(data)


def blacklist_refresh_token(refresh_token):
    result = {}
    try:
        token = RefreshToken(refresh_token)
        result['result'] = token.blacklist()[1] # (<BlacklistedToken: Blacklisted token for news356@gmail.com>, True)
        result['status'] = 'success'
    except TokenError as e:
        result['status'] = 'error'
        result['code'] = 'token_not_valid'
        result['detail'] = str(e)
    finally:
        return result

# SOCIAL ============================================================================================================================
def register_user_using_social_token(request):
    data = {}
    email = request.data.get('email', '0').lower()
    if validate_email(email) != None:
        data['error'] = 'That email is already in use.'
        data['status'] = 'error'
        return data
    
    account_type = request.data.get('account_type', None).lower()
    if account_type == None or is_valid_account_type(account_type) == False:
        data['error'] = 'The account type is not valid.'
        data['status'] = 'error'
        return data

    auth_token = request.data.get('auth_token', None)
    auth_token_data = is_valid_auth_token(account_type, auth_token)
    if auth_token == None or auth_token_data == None:
        data['error'] = 'The token is not valid.'
        data['status'] = 'error'
        return data   

    auth_token_data['account_type'] = account_type
    serializer = TokenRegistrationSerializer(data=auth_token_data)

    if serializer.is_valid():#we have transformed from json to python
        account = serializer.save()#Register User
        #the JWT token will contain the data I need about the user
        data = get_tokens_with_data(account)
    else:
        data['status'] = 'error'
        data['error'] = json.dumps(serializer.errors)
    return data

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view_jwt_social(request):
    if request.method == 'POST':
        data = register_user_using_social_token(request)        
        return Response(data)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def login_view_jwt_social(request):
    if request.method == 'POST':
        data = {}
       
        account_type = request.data.get('account_type', None).lower()
        if account_type == None or is_valid_account_type(account_type) == False:
            data['error'] = 'The account type is not valid.'
            data['status'] = 'error'
            return Response(data)

        auth_token = request.data.get('auth_token', None)
        auth_token_data = is_valid_auth_token(account_type, auth_token)
        if auth_token == None or auth_token_data == None:
            data['error'] = 'The token is not valid.'
            data['status'] = 'error'
            return Response(data)       
        
        account = get_account(auth_token_data['email'])
        if account != None:
            #account exists
            #the JWT token will contain the data I need about the user
            data = get_tokens_with_data(account)
        else:
            #account does not exists
            #so create a new one
            data = register_user_using_social_token(request)        
        return Response(data)
# ============================================================================================================================
def is_valid_auth_token(account_type, auth_token):
    data = {}
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(auth_token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        data['social_id'] = idinfo['sub']
        data['email'] = idinfo['email']
        data['fullname'] = idinfo['name']
        #data['picture'] = idinfo['picture']

    except Exception as e:
        print(str(e))
        # Invalid token
        data = None
    
    return data

def is_valid_account_type(account_type):
    valid = False
    if(account_type.lower() in SUPPORTED_ACCOUNT_TYPES ):
        valid = True
    return valid

def get_account(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return account

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
    permission_classes = [permissions.AllowAny]

    model = get_user_model()  # this is the model (dataset), so we need to pull out the data
    # Specify which serializer_class to use (show) when this view is accessed/served
    serializer_class = RegistrationSerializer
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
