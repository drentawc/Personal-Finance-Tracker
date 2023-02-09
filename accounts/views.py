from django.shortcuts import render
from accounts.models import User, Account

# Create your views here.

def account_index(request):
    accounts = Account.objects.all()

    context = {'accounts' : accounts}

    return render(request, 'account_index.html', context)


def account_detail(request, pk):
    accounts = Account.objects.get(pk=pk)

    context = {'accounts' : accounts}

    return render(request, 'account_detail.html', context)