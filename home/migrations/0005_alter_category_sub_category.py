# Generated by Django 4.2.9 on 2024-01-27 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_category_is_sub_category_sub_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scategory', to='home.category'),
        ),
    ]