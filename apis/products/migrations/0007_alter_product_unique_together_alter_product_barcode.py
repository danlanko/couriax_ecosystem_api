# Generated by Django 4.0.3 on 2022-03-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_business_account'),
        ('products', '0006_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('sku', 'business')},
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=50),
        ),
    ]
