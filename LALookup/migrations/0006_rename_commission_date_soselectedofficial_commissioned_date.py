# Generated by Django 4.2.11 on 2024-05-04 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LALookup", "0005_alter_soselectedofficial_commission_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="soselectedofficial",
            old_name="commission_date",
            new_name="commissioned_date",
        ),
    ]
