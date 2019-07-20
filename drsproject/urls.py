"""drsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from openspace.views import OpenSpaceView, NearSpaceViewSet, SpaceGeojsonViewSet, SpaceViewSet

urlpatterns = [
    path('', OpenSpaceView.as_view(), name="root"),
    path('api/', NearSpaceViewSet.as_view(), name="api"),
    path('api/add/', SpaceViewSet.as_view({'get': 'list','post':'create'}), name="space-add"),
    path('api/spaces/', SpaceGeojsonViewSet.as_view(), name="space"),
    path('admin/', admin.site.urls),
]
