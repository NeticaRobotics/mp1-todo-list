from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('data/<int:pk>/', views.DataOverview.as_view(), name='dataoverview'),

    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),
    # path('', views.Analytics.as_view(), name="analytics"),
]
