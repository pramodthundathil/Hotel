# Generated by Django 5.0.2 on 2024-03-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelbooking',
            name='special_Requests',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
