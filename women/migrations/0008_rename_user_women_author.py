# Generated by Django 4.2.6 on 2023-12-16 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0007_alter_women_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='women',
            old_name='user',
            new_name='author',
        ),
    ]
