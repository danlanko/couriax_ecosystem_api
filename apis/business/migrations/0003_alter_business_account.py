# Generated by Django 4.0.3 on 2022-03-28 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_remove_business_account_id_business_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='account',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='business.account'),
        ),
    ]
