from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.transaction_index, name="transaction_index"),
    path("<int:pk>/", views.transaction_detail, name="transaction_detail"),
]