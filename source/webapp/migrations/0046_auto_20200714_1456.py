# Generated by Django 2.2 on 2020-07-14 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0045_auto_20200714_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Order', verbose_name='Заказ'),
        ),
    ]