from django.db import models


class ListDeal(models.Model):
    CHOICES = [
        ('BTC', 'BTC'),
        ('ETH', 'ETH'),
        ('BNB', 'BNB'),
        ('TRX', 'TRX'),
        ('USDT', 'USDT'),
        ('USDC', 'USDC'),
        ('RUB', 'RUB'),
        ('EUR', 'EUR'),
        ('USD', 'USD'),
    ]

    STATUS = [
        ('Новая', 'Новая'),
        ('Проведена', 'Проведена'),
        ('Выплачена', 'Выплачена'),
    ]

    partner_id = models.BigIntegerField(blank=True, null=True, verbose_name='id партнера')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заявки')
    first_cur = models.CharField(max_length=10, choices=CHOICES, default='BTC', verbose_name='Входящая валюта')
    second_cur = models.CharField(max_length=10, choices=CHOICES, default='BTC', verbose_name='Исходящая валюта')
    first_amount = models.FloatField(blank=True, null=True, verbose_name='Входящая сумма')
    city = models.CharField(max_length=500, verbose_name='Город')
    second_amount = models.FloatField(blank=True, null=True, verbose_name='Исходящая сумма')
    profit = models.FloatField(blank=True, null=True, verbose_name='Доход партнера руб.')
    status = models.CharField(max_length=20, choices=STATUS, default='Новая', verbose_name='Статус выплаты')

    class Meta:
        verbose_name = 'сделку'
        verbose_name_plural = 'Список сделок'
        db_table = 'list_deal'
        ordering = ['id']
