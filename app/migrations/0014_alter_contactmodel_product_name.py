# Generated by Django 4.1.2 on 2023-11-08 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_contactmodel_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='product_name',
            field=models.CharField(default=False, max_length=30, verbose_name='商品名'),
        ),
    ]
