# Generated by Django 3.0 on 2023-03-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_orderlist_orderpending'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordersist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=100)),
                ('productid', models.CharField(max_length=100)),
                ('productname', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Orderlist',
        ),
    ]
