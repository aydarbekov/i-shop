# Generated by Django 2.2 on 2020-05-11 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20200511_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount',
            field=models.IntegerField(max_length=5, verbose_name='Количество'),
        ),
    ]
