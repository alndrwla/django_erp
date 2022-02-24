# Generated by Django 2.2 on 2021-04-15 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_auto_20210408_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='way_to_pay',
            field=models.CharField(choices=[('E', 'Efectivo'), ('C', 'Crédito')], default='E', max_length=10, verbose_name='Forma de pago'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categoría'),
        ),
    ]