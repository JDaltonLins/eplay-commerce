from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


urlpatterns = [
    path('/auth/login', render,
         {'template_name': 'auth/login.html'}, name='auth/login'),
    path('/auth/logoff', render,
         {'template_name': 'auth/login.html'}, name='auth/logoff'),
    path('/relatorios/', render,
         {'template_name': 'auth/login.html'}, name='relatorios/'),
]
