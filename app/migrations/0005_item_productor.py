# Generated by Django 4.1.2 on 2023-10-18 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='productor',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
