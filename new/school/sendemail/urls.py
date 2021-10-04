from django.contrib import admin
from django.urls import path

from .views import contact_view, success_view

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success'),
]