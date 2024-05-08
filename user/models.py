import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password


class CustomManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Укажите почту')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.create_activation_code()
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email", max_length=254, unique=True)
    objects = CustomManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    last_change_password = models.DateTimeField(null=True, blank=True, verbose_name='Последняя смена пароля')
    activation_code = models.CharField(max_length=40, blank=True, verbose_name='Активационный код')

    def __str__(self):
        return self.email

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code


class UserPasswords(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='last_passwords')  # TODO: related_name
    password = models.CharField(max_length=150, verbose_name='Пароль')  # TODO
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пароль пользователя'
        verbose_name_plural = 'Пароли пользователя'

    def __str__(self):
        return str(self.user)
