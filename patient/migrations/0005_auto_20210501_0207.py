# Generated by Django 3.1.3 on 2021-04-30 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20210501_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='diagnose_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.diagnose', verbose_name='诊断id'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='register_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.register', verbose_name='挂号id'),
        ),
    ]