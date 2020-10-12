from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.user import views

router = routers.DefaultRouter()
router.register('user', views.UserAPIView, basename='user')

urlpatterns = [
    url('', include(router.urls)),
]
