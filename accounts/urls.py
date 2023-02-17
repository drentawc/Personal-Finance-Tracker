from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [ 
    # path("", login_required(views.account_index), name="account_index"),
    # path("<int:pk>/", login_required(views.account_detail), name="account_detail"),
    path("", views.account_index, name="account_index"),
    path("<int:pk>/", views.account_detail, name="account_detail"),
]