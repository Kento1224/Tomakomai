# Generated by Django 3.2.16 on 2022-11-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_date', models.DateTimeField(verbose_name='日付')),
                ('detail', models.CharField(max_length=200)),
                ('cost', models.IntegerField(default=0)),
            ],
        ),
    ]