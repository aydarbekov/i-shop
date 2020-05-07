# Generated by Django 2.2 on 2020-05-06 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, verbose_name='Token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_tokens', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
