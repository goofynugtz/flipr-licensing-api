# Generated by Django 4.2.1 on 2023-05-11 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Licenses',
            new_name='License',
        ),
    ]
