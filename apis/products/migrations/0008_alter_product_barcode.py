# Generated by Django 4.0.3 on 2022-03-28 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_unique_together_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=50, null=True),
        ),
    ]