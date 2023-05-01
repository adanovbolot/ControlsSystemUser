from django.contrib.auth import logout
from django.db.models import Q
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    profile = models.CharField(
        verbose_name='Профиль',
        max_length=100
    )

    def __str__(self):
        return f"{self.profile}"


class Divisions(models.Model):
    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'подразделе́ний'

    divisions = models.CharField(
        verbose_name='Подразделение',
        max_length=100
    )

    def __str__(self):
        return f"{self.divisions}"


class Position(models.Model):
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'должности'

    position = models.CharField(
        verbose_name='Должность',
        max_length=100
    )

    def __str__(self):
        return f"{self.position}"


class UserAccess(models.Model):
    class Meta:
        verbose_name = 'Пользовательский доступ'
        verbose_name_plural = 'Пользовательский доступ'

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'

    )
    indicators = models.BooleanField(
        verbose_name='Показатель',
        default=False,
    )
    active = models.BooleanField(
        verbose_name='Активы',
        default=False
    )
    kp_russia = models.BooleanField(
        verbose_name='КП россия',
        default=False
    )
    kp_export = models.BooleanField(
        verbose_name='КП экспорт',
        default=False
    )
    kp_rent = models.BooleanField(
        verbose_name='КП аренда',
        default=False
    )
    production = models.BooleanField(
        verbose_name='Производство',
        default=False
    )
    car_park = models.BooleanField(
        verbose_name='Автопарк',
        default=False
    )
    staff = models.BooleanField(
        verbose_name='Персонал',
        default=False
    )
    notifications = models.BooleanField(
        verbose_name='Уведомления',
        default=False
    )

    def __str__(self):
        return f"{self.user}"


class UserSession(models.Model):
    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'

    )
    data_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Дата, время',
    )
    ip = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='IP'
    )
    client = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Клиент'
    )
    device_model = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Модель устройства'
    )
    app_version = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Версия App'
    )
    token = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Token'
    )
    received = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Получено'
    )
    transferred = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Передано'
    )
    access = models.BooleanField(
        verbose_name='Доступ',
        default=False
    )

    def __str__(self):
        return f"{self.user}"


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Номер',
        null=True,
        blank=True,
        unique=True
    )
    surname = models.CharField(
        verbose_name='Имя, Фамилия',
        max_length=100
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        verbose_name='Профиль',
        blank=True,
        null=True,
        related_name='profile_user'
    )
    divisions = models.ForeignKey(
        Divisions,
        on_delete=models.PROTECT,
        verbose_name='подразделение',
        related_name='divisions_user',
        blank=True,
        null=True
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name='Должность',
        related_name='position_user',
        blank=True,
        null=True
    )
    access = models.BooleanField(
        verbose_name='Доступ',
        default=False
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='персонал'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    status = models.BooleanField(
        verbose_name='Статус',
        default=False
    )
    reset_password_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        editable=False
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.email}" or f"{self.phone_number}"


class SessionTimeout(models.Model):
    class Meta:
        verbose_name = 'Таймаут сессии (сек)'
        verbose_name_plural = 'Таймаут сессии (сек)'

    session_timeout = models.PositiveIntegerField(
        default=30,
        verbose_name='Таймаут сессии (сек)'
    )

    def __str__(self):
        return f"{self.session_timeout}"


class ServerSettings(models.Model):
    class Meta:
        verbose_name_plural = 'Настройки сервера'
        verbose_name = 'Настройки сервера'

    session_timeout = models.ForeignKey(
        SessionTimeout,
        on_delete=models.PROTECT,
        verbose_name='Таймаут сессии (сек)'
    )
    server_url = models.CharField(
        max_length=50,
        verbose_name='Адрес сервера',
        blank=True,
        null=True
    )
    server_password = models.CharField(
        max_length=50,
        verbose_name='Пароль сервера',
        blank=True,
        null=True
    )
    dns = models.CharField(
        max_length=40,
        verbose_name='DNS',
        blank=True,
        null=True
    )
    ip = models.CharField(
        max_length=40,
        verbose_name='IP',
        blank=True,
        null=True
    )
    https = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='HTTPS'
    )
    ssl = models.CharField(
        verbose_name='SSL',
        max_length=50,
        blank=True,
        null=True
    )
    status_server = models.BooleanField(
        verbose_name='Сервер состояния',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.server_url}"

