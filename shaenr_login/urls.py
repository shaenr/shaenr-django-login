from django.urls import path, include
from django.contrib.auth.views import auth_login
from . import views

urlpatterns = [
    path('', views.index_page),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]