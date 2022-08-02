from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['partner_id', 'token', 'operator_id', 'operator_name', 'username', 'user_password']
    list_display_links = ['partner_id', 'token', 'operator_id', 'operator_name', 'username', 'user_password']
    fields = ['partner_id', 'token', 'operator_id', 'operator_name',  'username', 'user_password']


admin.site.register(CustomUser, CustomUserAdmin)
