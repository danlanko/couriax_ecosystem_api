# Generated by Django 4.0.3 on 2022-03-28 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_business_account'),
        ('products', '0003_alter_supplier_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='account',
            field=models.ForeignKey(default='b792ba87d4d44437a04078ee5c1ae533', on_delete=django.db.models.deletion.CASCADE, to='business.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.business'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
