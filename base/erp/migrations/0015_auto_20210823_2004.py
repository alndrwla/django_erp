# Generated by Django 2.2 on 2021-08-24 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0014_auto_20210823_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categoría'),
        ),
    ]
