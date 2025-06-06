# Generated by Django 4.2.20 on 2025-05-25 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0027_remove_campaign_campaign_id_alter_campaign_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="created",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="campaign",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="campaignprompt",
            name="created",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="campaignprompt",
            name="name",
            field=models.CharField(
                blank=True, db_index=True, max_length=200, null=True
            ),
        ),
        migrations.AddField(
            model_name="campaignprompt",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="campaignprompt",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="348fae346a8a434cabdb2e6ad9f4721c",
                max_length=40,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
