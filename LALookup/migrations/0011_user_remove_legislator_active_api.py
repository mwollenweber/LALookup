# Generated by Django 5.1.6 on 2025-03-18 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0010_legislator_officetitle"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("first_name", models.CharField(db_index=True, max_length=200)),
                ("last_name", models.CharField(db_index=True, max_length=200)),
                ("fullname", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "personalEmail",
                    models.CharField(
                        blank=True, db_index=True, max_length=200, null=True
                    ),
                ),
                ("homePhone", models.CharField(blank=True, max_length=200, null=True)),
                ("mobile", models.CharField(blank=True, max_length=200, null=True)),
                ("status", models.CharField(blank=True, max_length=200, null=True)),
                ("photoURL", models.CharField(blank=True, max_length=200, null=True)),
                ("gender", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "party",
                    models.CharField(
                        blank="U", db_index=True, max_length=200, null=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, db_index=True)),
                ("twitter", models.CharField(blank=True, max_length=200, null=True)),
                ("facebook", models.CharField(blank=True, max_length=200, null=True)),
                ("instagram", models.CharField(blank=True, max_length=200, null=True)),
                ("linkedin", models.CharField(blank=True, max_length=200, null=True)),
                ("youtube", models.CharField(blank=True, max_length=200, null=True)),
                ("website", models.CharField(blank=True, max_length=200, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("active", models.BooleanField(db_index=True, default=True)),
                ("api_key", models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="legislator",
            name="active",
        ),
        migrations.CreateModel(
            name="API",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="LALookup.user"
                    ),
                ),
            ],
        ),
    ]
