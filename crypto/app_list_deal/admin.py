from django.contrib import admin
from django.contrib.auth.models import Group
from .models import ListDeal
from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, FloatField, Count
from django.db.models.functions import Coalesce


class ListDealAdmin(ModelAdminTotals):
    list_display = ['partner_id', 'id', 'created_at', 'first_cur', 'second_cur',
                    'first_amount', 'city', 'second_amount', 'profit', 'status']
    list_display_links = ['partner_id', 'id', 'created_at', 'first_cur', 'second_cur']
    list_filter = ['partner_id', 'status']
    list_editable = ['first_amount', 'second_amount', 'profit', 'status']
    list_totals = [('id', lambda field: Coalesce(Count(field), 0)), ('profit', lambda field: Coalesce(Sum(field), 0, output_field=FloatField()))]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        else:
            return ['id', 'created_at', 'profit', 'status']

    def get_queryset(self, request):
        qs = super(ListDealAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(partner_id=request.user.partner_id)
        return qs


admin.site.register(ListDeal, ListDealAdmin)
admin.site.unregister(Group)
admin.site.site_title = 'Партнерский бот'
admin.site.site_header = 'Партнерский бот'
