# Generated by Django 4.2.11 on 2024-05-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LALookup', '0003_soselectedofficial_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soselectedofficial',
            old_name='officeParish',
            new_name='parish',
        ),
        migrations.AddField(
            model_name='soselectedofficial',
            name='phone',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]