# Generated by Django 2.2 on 2020-08-06 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0052_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colors', to='webapp.Color', verbose_name='Цвет'),
        ),
    ]
