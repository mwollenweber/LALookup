# Generated by Django 4.2.20 on 2025-05-20 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0017_request"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="addressText",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="request",
            name="lat",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="request",
            name="lon",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="request",
            name="referrer",
            field=models.TextField(null=True),
        ),
    ]
