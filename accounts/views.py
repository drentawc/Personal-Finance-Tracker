from django.shortcuts import render
from accounts.models import User, Account

# Create your views here.


#

def account_index(request):
    accounts = Account.objects.all()

    creditAccounts = Account.objects.filter(accounttype__icontains='credit').all()
    checkingAccounts = Account.objects.filter(accounttype__icontains='checking').all()
    savingsAccounts = Account.objects.filter(accounttype__icontains='saving').all()
    investmentAccounts = Account.objects.filter(accounttype__icontains='investment').all()

    #creditAccounts = Account.get

    context = {'accounts' : accounts, 'credit' : creditAccounts, 'checking' : checkingAccounts, 'saving' : savingsAccounts, 'invest' : investmentAccounts}

    return render(request, 'account_index.html', context)


def account_detail(request, pk):
    accounts = Account.objects.get(pk=pk)

    context = {'accounts' : accounts}

    return render(request, 'account_detail.html', context)