from django.contrib.auth.models import AbstractUser
from django.db import models



NULLABLE = {'blank': True, 'null': True}
# Create your models here.

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=40, verbose_name='номер телефона')
    country = models.CharField(max_length=70, **NULLABLE, verbose_name='страна')
    avatar = models.ImageField(upload_to='', **NULLABLE, verbose_name='аватар')
    email = models.EmailField(unique=True, verbose_name='почта')
    is_active = models.BooleanField("active", default=False, help_text=(   # Статус
        "Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts."
    )
                                    )
    cod = models.CharField(unique=True, **NULLABLE, verbose_name='код')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
