# Generated by Django 4.0.6 on 2022-07-15 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_crypto', '0006_customuser_operator_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='operator_name',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Username оператора'),
        ),
    ]
