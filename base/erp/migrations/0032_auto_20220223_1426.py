# Generated by Django 2.2 on 2022-02-23 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0031_auto_20210920_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Category', verbose_name='Categoría'),
        ),
    ]
