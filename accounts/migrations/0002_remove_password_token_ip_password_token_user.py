# Generated by Django 4.2 on 2025-03-06 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="password_token",
            name="ip",
        ),
        migrations.AddField(
            model_name="password_token",
            name="user",
            field=models.OneToOneField(
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
