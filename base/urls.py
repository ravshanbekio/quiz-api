from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

router = routers.DefaultRouter()
router.register('rating',ReytingViewSet)
router.register('soha',SohaViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('',include(router.urls))
]