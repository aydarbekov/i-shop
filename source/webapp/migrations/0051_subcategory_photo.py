# Generated by Django 2.2 on 2020-08-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0050_auto_20200731_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='subcategory_images', verbose_name='Изображение'),
        ),
    ]