# Generated by Django 4.2.20 on 2025-05-25 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0023_client_campaign"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="campaign_id",
            field=models.CharField(blank=True, db_index=True, max_length=40),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="campaign_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="b4d13174026f4a5180ddb273770d011e",
                max_length=40,
            ),
        ),
    ]
