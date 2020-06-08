from rest_framework.authtoken import views as authviews
from django.urls import path

from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('api/token-auth-login/', authviews.obtain_auth_token, name='login_token'),
    path('api/token-auth-signup/', views.registration_view, name='signup_token'),
    path('api/no-token-signup/', views.RegisterUserOnlyView.as_view(), name='signup_no_token'),
    path('test/labels/', views.TestAllLabels.as_view(), name='test'),
]