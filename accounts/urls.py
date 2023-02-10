from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.account_index, name="account_index"),
    path("<int:pk>/", views.account_detail, name="account_detail"),
]