# Generated by Django 3.1.3 on 2021-04-21 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20210421_0109'),
        ('doctor', '0004_auto_20210421_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckDetail',
            fields=[
                ('detail_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='详情id')),
                ('report_content', models.CharField(max_length=200, verbose_name='检查结果')),
                ('check_time', models.DateField(verbose_name='检查时间')),
                ('check_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.checkitem', verbose_name='检查id')),
                ('diagnose_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.diagnose', verbose_name='诊断id')),
            ],
            options={
                'verbose_name': '检查详情',
                'verbose_name_plural': '检查详情',
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('report_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='检查id')),
                ('check_list', models.CharField(max_length=100, verbose_name='检查内容')),
                ('chest', models.PositiveIntegerField(choices=[(1, '胸痛'), (0, '正常')], default=0, verbose_name='症状')),
                ('diagnose_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.diagnose', verbose_name='诊断id')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patientbase', verbose_name='病人号')),
            ],
            options={
                'verbose_name': '检查信息',
                'verbose_name_plural': '检查信息',
            },
        ),
    ]
