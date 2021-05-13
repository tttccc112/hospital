# Generated by Django 3.1.3 on 2021-05-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_auto_20210501_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patienthealth',
            name='cTnI',
            field=models.IntegerField(blank=True, null=True, verbose_name='肌钙蛋白I'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='ct',
            field=models.IntegerField(blank=True, null=True, verbose_name='胸痛'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='pgender',
            field=models.IntegerField(blank=True, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='q',
            field=models.IntegerField(blank=True, null=True, verbose_name='病理性Q波'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='std',
            field=models.IntegerField(blank=True, null=True, verbose_name='ST-T压低'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='stt',
            field=models.IntegerField(blank=True, null=True, verbose_name='ST-T改变'),
        ),
        migrations.AlterField(
            model_name='patienthealth',
            name='stup',
            field=models.IntegerField(blank=True, null=True, verbose_name='ST-T抬高'),
        ),
    ]
