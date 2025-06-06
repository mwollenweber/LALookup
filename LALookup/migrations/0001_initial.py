# Generated by Django 4.2.11 on 2024-05-04 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Legislator",
            fields=[
                ("first_name", models.CharField(max_length=200)),
                ("last_name", models.CharField(max_length=200)),
                ("fullname", models.CharField(blank=True, max_length=200, null=True)),
                ("active", models.BooleanField(default=True)),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
                ("homePhone", models.CharField(blank=True, max_length=200, null=True)),
                ("mobile", models.CharField(blank=True, max_length=200, null=True)),
                ("status", models.CharField(blank=True, max_length=200, null=True)),
                ("photoURL", models.CharField(blank=True, max_length=200, null=True)),
                ("gender", models.CharField(blank=True, max_length=200, null=True)),
                ("party", models.CharField(blank=True, max_length=200, null=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now=True)),
                ("chamber", models.CharField(default="house", max_length=200)),
                ("districtnumber", models.IntegerField(default=0)),
                (
                    "officeaddress",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "officePhone",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
