# Generated by Django 2.2 on 2021-09-03 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0025_auto_20210903_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paychecks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numCheck', models.CharField(max_length=10, verbose_name='Cheque N.')),
                ('name', models.CharField(max_length=100, verbose_name='Páguese a la orden de')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='US')),
                ('plus', models.CharField(max_length=250, verbose_name='La suma de ')),
                ('place', models.CharField(max_length=100, verbose_name='Ciudad')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('payChoice', models.CharField(choices=[('C', 'PEDIENTE'), ('P', 'PAGADO')], default='C', max_length=1, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Detalle de Cheque',
                'verbose_name_plural': 'Detalle de Cheques',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categoría'),
        ),
    ]
