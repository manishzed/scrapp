# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:12:41 2019

@author: hp
"""

from app import views 
from app.views import scrap
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
 


app_name = 'app'

urlpatterns = [
    path('scrap/', views.scrap, name="scrap"),
]