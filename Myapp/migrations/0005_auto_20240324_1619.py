# Generated by Django 3.0 on 2024-03-24 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_device_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='DEVICE',
        ),
        migrations.CreateModel(
            name='BookingSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DEVICE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.Device')),
            ],
        ),
    ]
