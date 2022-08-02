from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from app_list_deal.models import ListDeal


class CustomUser(AbstractUser):
    partner_id = models.BigIntegerField(blank=True, null=True, verbose_name='id партнера')
    token = models.CharField(max_length=500, blank=True, null=True, verbose_name='TG Токен Бота')
    operator_id = models.BigIntegerField(blank=True, null=True, verbose_name='id оператора')
    operator_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='Username оператора')
    user_password = models.CharField(max_length=100, blank=True, null=True, verbose_name='Пароль партнера')

    def amount_status(self):
        amo = ListDeal.objects.filter(partner_id=self.partner_id, status=True).aggregate(Sum('profit'))['profit__sum']
        if amo is not None:
            return amo
        else:
            return 0.0

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

