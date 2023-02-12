from django.shortcuts import render
from transactions.models import Transaction
from accounts.models import Account

# Create your views here.

def transaction_index(request):
    transactions = Transaction.objects.all()

    #need to figure out how to filter on the account, and then concat all accounts of a certain type 
    #creditTransactions = Transaction.objects.filter(accountid__)

    creditAccounts = Account.objects.filter(accounttype__icontains='credit').all()
    checkingAccounts = Account.objects.filter(accounttype__icontains='checking').all()
    savingsAccounts = Account.objects.filter(accounttype__icontains='saving').all()
    investmentAccounts = Account.objects.filter(accounttype__icontains='investment').all()

    #creditAccounts = Account.objects.filter(accounttype__icontains='checking').all()

    #Currently working on a way to return a list of certain accounts, can maybe 

    creditTransactions = []
    # for trans in transactions:
    #     for account in creditAccounts:
    #         if trans.
    #         creditTransactions.append(account)

    creditTransactions = None

    for account in creditAccounts:
        if creditTransactions is None:
            creditTransactions = Transaction.objects.filter(accountid=account.accountid).all()
        else:
            creditTransactions = creditTransactions | Transaction.objects.filter(accountid=account.accountid).all()

    checkingTransactions = []
    for account in checkingAccounts:
        checkingTransactions.append(account)

    savingTransactions = []
    for account in savingsAccounts:
        savingTransactions.append(account)

    investmentTransactions = []
    for account in investmentAccounts:
        investmentTransactions.append(account)
    #creditTransactions = Transaction.objects.filter(accountid=creditAccount['accountid'].value()).all()

    #creditAccounts = Account.get

    context = {'transactions' : transactions, 'credit' : creditTransactions.order_by('-date')[0:50], 'checking' : checkingTransactions, 'saving' : savingTransactions, 'invest' : investmentTransactions}

    return render(request, 'transaction_index.html', context)

def transaction_detail(request, pk):
    transactions = Transaction.objects.get(pk=pk)

    context = {'transactions' : transactions}

    return render(request, 'account_detail.html', context)
