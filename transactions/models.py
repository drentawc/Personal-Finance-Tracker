from django.db import models

# Create your models here.

class Transaction(models.Model):
    transactionid = models.AutoField(db_column='transactionId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('accounts.User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    accountid = models.ForeignKey('accounts.Account', models.DO_NOTHING, db_column='accountId')  # Field name made lowercase.
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    transactionnumber = models.CharField(db_column='transactionNumber', unique=True, max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transactions'