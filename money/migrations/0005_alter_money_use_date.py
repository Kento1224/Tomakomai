# Generated by Django 3.2.16 on 2022-11-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_money_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='use_date',
            field=models.DateField(),
        ),
    ]