#!/bin/python3


"""badi URL Configuration

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

from .views.init import InitView
from .views.sunlight_hours import SunlightHoursView
from .views.default import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('init', InitView.as_view()),
    path('sunlight_hours', SunlightHoursView.as_view()),
    path('get_sunlight_hours', SunlightHoursView.as_view()),
    path('getSunlightHours', SunlightHoursView.as_view()),

]

handler404 = handler404
handler500 = handler500
