# Generated by Django 3.2.4 on 2021-06-25 07:11

import app_account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[app_account.models.phone_validate])),
                ('name', models.CharField(max_length=150)),
                ('register_date', models.DateTimeField(blank=True, null=True)),
                ('confirm_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_seller', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
