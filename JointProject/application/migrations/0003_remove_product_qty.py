# Generated by Django 2.1.7 on 2019-05-19 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_remove_manifest_withdrawal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='qty',
        ),
    ]
