# Generated by Django 5.1.3 on 2024-12-05 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_chanel_otprequest_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='password',
            field=models.CharField(default='5518', max_length=4),
        ),
    ]