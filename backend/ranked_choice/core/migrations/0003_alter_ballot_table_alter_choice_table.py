# Generated by Django 4.2.23 on 2025-07-05 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_choice_created_at_choice_updated_at'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ballot',
            table='ballot',
        ),
        migrations.AlterModelTable(
            name='choice',
            table='choice',
        ),
    ]
