from django.urls import path, include
from . import views
from rest_framework import routers # allows us to create GET and POST requests

#1)create router
router = routers.DefaultRouter()
#2)register view with the RestFramework so we can see them in the Rest Framework homepage as links
router.register('all', views.SyncUpAllView) # 1st param -> url to access this view, 2nd param -> the view extending rest_framework viewsets.ModelViewSet
urlpatterns = [
    path('', include(router.urls)),
    path('check/', views.ServerDBVersionView.as_view(), name='check_latest_version'),
    path('process/', views.ServerSyncUpDBProcessView.as_view(), name='process_data'),
    # path('syncup/', views.ServerDBSyncUpView.as_view(), name='syncup_data'),

    # path('type/<str:resource_type>/', views.ResourcesByTypeView.as_view(), name='resources_type'),
    # path('language/<str:language>/', views.ResourcesByLangView.as_view(), name='resources_lang'),
]