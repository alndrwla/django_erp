# Generated by Django 2.2 on 2021-09-03 15:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0024_auto_20210827_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salepayment',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Venta a crédito', 'verbose_name_plural': 'Detalle de Ventas a crédito'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categoría'),
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('sale_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.SaleLocation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Guía',
                'verbose_name_plural': 'Guías',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DetGuide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Guide')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Product')),
            ],
            options={
                'verbose_name': 'Detalle de Guía',
                'verbose_name_plural': 'Detalle de Guías',
                'ordering': ['id'],
            },
        ),
    ]