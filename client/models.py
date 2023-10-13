from django.db import models

from user.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):  # Клиент сервиса
    email = models.EmailField(verbose_name='Почта для рассылки')
    full_name = models.CharField(**NULLABLE, verbose_name='Имя', max_length=150)
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Собственник')

    def __str__(self):
        return f'{self.comment} {self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):  # Рассылка (настройки)

    PERIOD_DAILY = 'Ежедневная'
    PERIOD_WEEKLY = 'Раз в неделю'
    PERIOD_MONTHLY = 'Раз в месяц'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_DONE = 'Завершена'

    STATUSES = (
        (STATUS_STARTED, 'Создана'),
        (STATUS_CREATED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    )

    start_time = models.DateTimeField(**NULLABLE, verbose_name='Начало рассылки')
    end_time = models.DateTimeField(**NULLABLE, verbose_name='Конец рассылки')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус рассылки')

    clients = models.ManyToManyField('Client', verbose_name='клиенты')  # Многи к многим
    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Собственник')
    def __str__(self):
        return f'{self.start_time} / {self.end_time}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


# class MailingClient(models.Model):   #!!!!
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
#     settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')
#
#     def __str__(self):
#         return f'{self.client} / {self.settings}'
#
#     class Meta:
#         verbose_name = 'Клиент рассылки'
#         verbose_name_plural = 'Клиенты рассылки'


class MailingMessage(models.Model):  # Сообщение для рассылки
    subject = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(verbose_name='текст')

    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE, verbose_name='Собственник')
    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingLog(models.Model):  # Логи рассылки
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey('MailingSettings', on_delete=models.CASCADE, verbose_name='Настройка')

    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус попытки')
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    answer = models.TextField(**NULLABLE, verbose_name='ответ')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
