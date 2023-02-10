from django.db import models

# Create your models here.

class User(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=20)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=20)  # Field name made lowercase.
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('firstname', 'lastname'),)

class Account(models.Model):
    accountid = models.AutoField(db_column='accountId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    bankname = models.CharField(db_column='bankName', max_length=50)  # Field name made lowercase.
    lastfour = models.CharField(db_column='lastFour', max_length=4)  # Field name made lowercase.
    description = models.CharField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    accounttype = models.CharField(db_column='accountType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accountnumber = models.CharField(db_column='accountNumber', max_length=30)  # Field name made lowercase.

    def toString(self):
        return self.bankname

    # def get_url(self):
    #     curr = Account.objects.first()
    #     return curr.accounttype
        #return Account.objects.filter(accounttype__icontains='credit').all()
        # prefetch = Prefetch('account_set', queryset=Account.objects.filter(accounttype_contains='CREDIT'), to_attr="credit_accounts")
        # return Account.objects.filter

    # def getCheckingAccounts(self):
    #     return Account.objects.filter(accounttype_contains='CHECKING').all()

    # def getSavingAccounts(self):
    #     return Account.objects.filter(accounttype_contains='SAVING').all()

    # def getSavingAccounts(self):
    #     return Account.objects.filter(accounttype_contains='Investment').all()

    class Meta:
        managed = False
        db_table = 'accounts'
        unique_together = (('lastfour', 'accountnumber'),)
