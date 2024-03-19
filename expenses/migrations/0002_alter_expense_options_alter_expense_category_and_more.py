# Generated by Django 5.0.3 on 2024-03-16 09:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={},
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(max_length=266),
        ),
        migrations.AlterField(
            model_name='expense',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]