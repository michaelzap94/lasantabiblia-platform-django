from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,)#OR HyperlinkedModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Since I'm using a custom User, I need to import the custom User class and not the Built-in model
from Account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    #password number 2 is not part of the Account model, so when you add it to fields:
    #fields = ( "id", "email", "password", "password2", "fullname" )
    #it will trow an error unless we specify this field here
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def create(self, validated_data):
        account = Account(
            email=validated_data['email'], 
            fullname=validated_data.get('fullname', None), 
            firstname=validated_data.get('firstname', None), 
            lastname=validated_data.get('lastname', None))
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

    # def save(self): # If you implement this, you'll have to call .save on the Account object in the views.py file
    #     account = Account(email=self.validated_data['email'])
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']
    #     if password != password2:
    #         raise serializers.ValidationError({'password': 'Passwords must match.'})
    #     account.set_password(password)
    #     account.save()
    #     return account
        
    class Meta:
        model = Account
        fields = ( "id", "email", "password", "password2", "fullname", "firstname", "lastname" )
        extra_kwargs = {
            'password' : {'write_only': True} # we don't want the password to be readable, only writable
        }

#IMPORT THE DJANGO BUILT-IN ADMIN Model 'User'
#from django.contrib.auth.models import User #SAME AS:
#from django.contrib.auth import get_user_model # Return User Model that is Active in this project
# UserModel = get_user_model()

#Serialize JWT login/signup data returned in jwt token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, account):
        # The default result (access/refresh tokens)
        token = super().get_token(account)
        # Add custom claims
        token['email'] = account.email
        token['fullname'] = account.fullname
        token['firstname'] = account.firstname
        token['lastname'] = account.lastname
        return token
    
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include in the response object
        data.update({'status': 'success'})
        #data.update({'id': self.user.id}) #id is already included in the JWT token
        # and everything else you want to send in the response
        return data
