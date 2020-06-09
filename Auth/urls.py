#THESE pre-packaged mthods will need 'username', you can also use your own methods
from rest_framework.authtoken import views as authviews
from rest_framework_simplejwt import views as jwt_views

from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    #Token
    path('api/token/signup/', views.registration_view, name='signup_token'),
    #you can use a custom view if you need to return more data apart from token(this requires 'username')
    path('api/token/login/', authviews.obtain_auth_token, name='login_token'),
    #JWT
    path('api/jwt/signup/', views.registration_view_jwt, name='signup_jwt'),
    #path('api/jwt/login/', jwt_views.TokenObtainPairView.as_view(), name='login_jwt'), #built-in login
    path('api/jwt/login/', views.MyTokenObtainPairView.as_view(), name='login_jwt'),
    path('api/jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh_jwt'),
    path('api/jwt/logout/', views.logout_view_jwt, name='logout_jwt'),
    #EXTRA
    path('api/no-token/signup/', views.RegisterUserOnlyView.as_view(), name='signup_no_token'),
    path('test/labels/', views.TestAllLabels.as_view(), name='test'),
]