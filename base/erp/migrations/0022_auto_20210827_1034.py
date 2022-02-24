# Generated by Django 2.2 on 2021-08-27 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0021_auto_20210827_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='total_first_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.Category', verbose_name='Categoría'),
        ),
    ]