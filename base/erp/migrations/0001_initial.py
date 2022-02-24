# Generated by Django 2.2 on 2021-03-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre de la empresa')),
                ('ruc', models.CharField(max_length=15, verbose_name='Ruc')),
                ('tax', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Tasa de interes')),
                ('facebook', models.URLField(max_length=250, verbose_name='Direcciòn de facebook')),
                ('whatsapp', models.URLField(max_length=250, verbose_name='Direcciòn de whatsapp')),
                ('state', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]