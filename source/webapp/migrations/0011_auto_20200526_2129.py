# Generated by Django 2.2 on 2020-05-26 21:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, verbose_name='Название')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='brand_images', verbose_name='Изображение')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='photo',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, choices=[('#F0DEBA;', 'Бежевый'), ('green', 'Зеленый'), ('grey', 'Серый'), ('blue', 'Синий'), ('red', 'Красный'), ('yellow', 'Желтый'), ('black', 'Черный'), ('orange', 'Оранжевый'), ('brown', 'Коричневый'), ('white', 'Белый'), ('pink', 'Розовый'), ('purple', 'Фиолетовый'), ('darkblue', 'Темно-синий'), ('darkgreen', 'Темно-зеленый')], default='#F0DEBA;', max_length=20, null=True, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата добавления'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=3000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='webapp.Brand', verbose_name='Бренд'),
        ),
    ]