# Generated by Django 4.2.20 on 2025-05-20 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0021_alter_log_id_alter_request_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="user_agent",
            field=models.TextField(blank=True, null=True),
        ),
    ]
