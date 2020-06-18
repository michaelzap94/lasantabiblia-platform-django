from django.urls import path, include
from . import views
from rest_framework import routers # allows us to create GET and POST requests

#1)create router
router = routers.DefaultRouter()
#2)register view with the RestFramework so we can see them in the Rest Framework homepage as links
router.register('labels', views.LabelView) # 1st param -> url to access this view, 2nd param -> the view extending rest_framework viewsets.ModelViewSet
router.register('verses_marked', views.VersesMarkedView) # 1st param -> url to access this view, 2nd param -> the view extending rest_framework viewsets.ModelViewSet
router.register('verses_learned', views.VersesLearnedView) # 1st param -> url to access this view, 2nd param -> the view extending rest_framework viewsets.ModelViewSet

urlpatterns = [
    path('', include(router.urls)),
]