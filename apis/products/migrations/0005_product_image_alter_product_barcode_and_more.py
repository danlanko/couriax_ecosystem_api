# Generated by Django 4.0.3 on 2022-03-28 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_business_account'),
        ('products', '0004_supplier_account_alter_supplier_business_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='user_avatar'),
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.business'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.account'),
        ),
    ]
