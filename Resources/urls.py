from django.urls import path, include
from . import views
from rest_framework import routers # allows us to create GET and POST requests

#1)create router
router = routers.DefaultRouter()
#2)register view with the RestFramework so we can see them in the Rest Framework homepage as links
router.register('all', views.ResourcesAllView) # 1st param -> url to access this view, 2nd param -> the view extending rest_framework viewsets.ModelViewSet
urlpatterns = [
    #path('all/', views.ResourcesAllView.as_view(), name='resources_all'),
    path('', include(router.urls)),
    path('type/<str:resource_type>/', views.ResourcesByTypeView.as_view(), name='resources_type'),
    path('language/<str:language>/', views.ResourcesByLangView.as_view(), name='resources_lang'),
    path('extra/', views.ResourcesExtraView.as_view(), name='resources_extra'),
]