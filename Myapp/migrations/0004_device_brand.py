# Generated by Django 3.0 on 2024-03-19 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_auto_20240225_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='brand',
            field=models.CharField(default='', max_length=30),
        ),
    ]