from django.shortcuts import render
from accounts.models import User, Account
# Create your views here.

def homepage(request):
    users = User.objects.all()

    context = {'users' : users}

    return render(request, 'homepage.html', context)
