"""finance_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [

    #@TODO figure out if want homepage as seperate django app or just as template, might be nice to have as seperate app for models

    #path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('', include("homepage.urls")),
    path('admin/', admin.site.urls),
    path('log/', include("django.contrib.auth.urls")),
    path('accounts/', include("accounts.urls")),
    path('transactions/', include("transactions.urls")),

]
