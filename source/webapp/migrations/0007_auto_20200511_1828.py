# Generated by Django 2.2 on 2020-05-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20200511_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount',
            field=models.IntegerField(verbose_name='Количество'),
        ),
    ]
