# Generated by Django 2.2.4 on 2020-12-04 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_buddy_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
