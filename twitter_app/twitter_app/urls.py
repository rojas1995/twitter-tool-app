"""twitter_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import login
from api import views


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/login', login),
    path('admin/', admin.site.urls),
    path('', views.GetAPIData.as_view(template_name='home.html'), name='home'),
    path('jobs/', views.GetAPIData.as_view(template_name='data_view.html'), name='Data View'),
    path('form/', views.GetForm.as_view(template_name='request_form.html'), name='Data Form View'),
    path('success/', views.GetForm.as_view(template_name='success_form.html'), name='success')

]

handler404 = 'api.views.error_404_view'




