# Generated by Django 5.1.3 on 2024-12-05 10:42

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_otprequest_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='password',
            field=models.CharField(default=user.models.generate_otp, max_length=4),
        ),
    ]