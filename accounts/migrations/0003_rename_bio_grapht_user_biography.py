# Generated by Django 5.2 on 2025-04-21 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='bio_grapht',
            new_name='biography',
        ),
    ]
