from .views import *

from django.urls import path

from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


urlpatterns = [
    path('coins/', getCoins.as_view(), name='All devices'),

]
