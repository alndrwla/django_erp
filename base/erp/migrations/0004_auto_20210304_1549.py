# Generated by Django 2.2 on 2021-03-04 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='dealer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Dealer', verbose_name='Distribuidor'),
        ),
        migrations.CreateModel(
            name='SaleLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre del local')),
                ('direction', models.CharField(max_length=50, verbose_name='Direcciòn de la empresa')),
                ('state', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Business', verbose_name='Empresa')),
            ],
        ),
    ]
