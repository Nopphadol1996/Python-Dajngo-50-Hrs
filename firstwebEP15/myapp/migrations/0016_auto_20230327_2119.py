# Generated by Django 3.0 on 2023-03-27 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20230327_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderlist',
            old_name='orderid1',
            new_name='orderid',
        ),
        migrations.RenameField(
            model_name='orderpending',
            old_name='orderid1',
            new_name='orderid',
        ),
    ]
