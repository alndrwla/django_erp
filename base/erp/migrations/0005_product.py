# Generated by Django 2.2 on 2021-03-04 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_auto_20210304_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Còdigo del producto')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del producto')),
                ('description', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripciòn del producto')),
                ('stock', models.IntegerField(default=0, verbose_name='Cantidad de producto')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio unitario neto')),
                ('sale_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de venta')),
                ('state', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categorìa')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Dealer', verbose_name='Distribuidor')),
                ('sale_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.SaleLocation', verbose_name='Local de ventas')),
            ],
        ),
    ]
