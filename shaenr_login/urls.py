from django.urls import path, include
from django.contrib.auth.views import auth_login
from . import views as shaenr_login_views
from django.contrib import admin

urlpatterns = [
    path('', shaenr_login_views.index_page, name='index'),
    path('register/', shaenr_login_views.register, name='register')
]

urlpatterns += [
    path('accounts/', shaenr_login_views.listing, name='listing'),
    path('accounts/profile/<int:_id>', shaenr_login_views.view_user, name='view_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("see_request/", shaenr_login_views.see_request),
    path('accounts/verify/<uidb64>/<token>', shaenr_login_views.verify_email, name='email_verify'),
    path('admin/', admin.site.urls),
]