# Generated by Django 3.2.16 on 2022-11-30 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_alter_money_use_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='money',
            name='cost',
        ),
    ]
