from django.db import models

# Create your models here.
# class User(models.Model):
#     userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
#     firstname = models.CharField(db_column='firstName', max_length=20)  # Field name made lowercase.
#     lastname = models.CharField(db_column='lastName', max_length=20)  # Field name made lowercase.
#     password = models.CharField(max_length=20)

#     class Meta:
#         managed = False
#         db_table = 'users'
#         unique_together = (('firstname', 'lastname'),)