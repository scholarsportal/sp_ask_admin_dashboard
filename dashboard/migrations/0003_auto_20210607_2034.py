# Generated by Django 2.2.19 on 2021-06-08 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0002_auto_20210607_2032"),
    ]

    operations = [
        migrations.RenameField(
            model_name="referencequestion",
            old_name="anonymized_message",
            new_name="message",
        ),
        migrations.AddField(
            model_name="referencequestion",
            name="is_anonymized",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
