# Generated by Django 3.2 on 2022-04-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my8gag', '0006_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
