# Generated by Django 4.2.6 on 2023-11-04 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0005_alter_tagwomen_options_alter_tagwomen_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/', verbose_name='Фотография'),
        ),
    ]
