# Generated by Django 3.1 on 2023-04-17 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_is_availabe_product_is_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
