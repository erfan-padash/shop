# Generated by Django 5.0 on 2024-01-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_category_options_alter_product_imagefield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imagefield',
            field=models.ImageField(upload_to=''),
        ),
    ]
