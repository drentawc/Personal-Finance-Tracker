# Generated by Django 4.1.5 on 2023-02-10 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('accountid', models.AutoField(db_column='accountId', primary_key=True, serialize=False)),
                ('bankname', models.CharField(db_column='bankName', max_length=50)),
                ('lastfour', models.CharField(db_column='lastFour', max_length=4)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('accounttype', models.CharField(blank=True, db_column='accountType', max_length=20, null=True)),
                ('accountnumber', models.CharField(db_column='accountNumber', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(db_column='userId', primary_key=True, serialize=False)),
                ('firstname', models.CharField(db_column='firstName', max_length=20)),
                ('lastname', models.CharField(db_column='lastName', max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='Accounts',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.AddField(
            model_name='account',
            name='userid',
            field=models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.user'),
        ),
    ]