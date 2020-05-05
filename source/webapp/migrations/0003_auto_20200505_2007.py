# Generated by Django 2.2 on 2020-05-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=50, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sub_name',
            field=models.CharField(max_length=50, verbose_name='Подраздел'),
        ),
    ]
