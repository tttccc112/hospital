# Generated by Django 3.1.3 on 2021-06-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_auto_20210504_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '未缴费'), (1, '已缴费')], default=1, verbose_name='缴费状态'),
        ),
    ]