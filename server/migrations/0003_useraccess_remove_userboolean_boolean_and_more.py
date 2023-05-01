# Generated by Django 4.2 on 2023-04-30 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_user_user_boolean'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicators', models.BooleanField(default=False, verbose_name='Показатель')),
                ('active', models.BooleanField(default=False, verbose_name='Активы')),
                ('kp_russia', models.BooleanField(default=False, verbose_name='КП россия')),
                ('kp_export', models.BooleanField(default=False, verbose_name='КП экспорт')),
                ('kp_rent', models.BooleanField(default=False, verbose_name='КП аренда')),
                ('production', models.BooleanField(default=False, verbose_name='Производство')),
                ('car_park', models.BooleanField(default=False, verbose_name='Автопарк')),
                ('staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('notifications', models.BooleanField(default=False, verbose_name='Уведомления')),
            ],
        ),
        migrations.RemoveField(
            model_name='userboolean',
            name='boolean',
        ),
        migrations.RemoveField(
            model_name='userboolean',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_boolean',
        ),
        migrations.DeleteModel(
            name='Boolean',
        ),
        migrations.DeleteModel(
            name='UserBoolean',
        ),
        migrations.AddField(
            model_name='useraccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
