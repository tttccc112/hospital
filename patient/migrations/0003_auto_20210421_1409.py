# Generated by Django 3.1.3 on 2021-04-21 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_check_checkdetail'),
        ('patient', '0002_auto_20210421_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnose',
            name='report_id',
            field=models.ForeignKey(default='REPORT0', on_delete=django.db.models.deletion.CASCADE, to='doctor.check', verbose_name='检查id'),
        ),
        migrations.CreateModel(
            name='Prescribe',
            fields=[
                ('prescribe_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='开药id')),
                ('prescribe_content', models.CharField(max_length=100, verbose_name='开药记录')),
                ('diagnose_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.diagnose', verbose_name='诊断id')),
            ],
            options={
                'verbose_name': '开药信息',
                'verbose_name_plural': '开药信息',
            },
        ),
        migrations.CreateModel(
            name='PatientHealth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdate', models.DateField(verbose_name='入院时间')),
                ('pgender', models.BinaryField(blank=True, null=True, verbose_name='性别')),
                ('page', models.IntegerField(blank=True, null=True, verbose_name='就诊年龄')),
                ('low_bp', models.IntegerField(blank=True, null=True, verbose_name='舒张压')),
                ('high_bp', models.IntegerField(blank=True, null=True, verbose_name='收缩压')),
                ('ast', models.IntegerField(blank=True, null=True, verbose_name='天门冬氨酸氨基转移酶')),
                ('alat', models.IntegerField(blank=True, null=True, verbose_name='丙氨酸氨基转移酶')),
                ('tp', models.FloatField(blank=True, null=True, verbose_name='总蛋白')),
                ('alb', models.FloatField(blank=True, null=True, verbose_name='白蛋白')),
                ('glb', models.FloatField(blank=True, null=True, verbose_name='球蛋白')),
                ('ag', models.FloatField(blank=True, null=True, verbose_name='白球蛋白比值')),
                ('tg', models.FloatField(blank=True, null=True, verbose_name='甘油三酯')),
                ('tc', models.FloatField(blank=True, null=True, verbose_name='总胆固醇')),
                ('glc', models.FloatField(blank=True, null=True, verbose_name='葡萄糖测定')),
                ('hdl', models.FloatField(blank=True, null=True, verbose_name='高密度脂蛋白胆固醇')),
                ('ldl', models.FloatField(blank=True, null=True, verbose_name='低密度脂蛋白胆固醇')),
                ('cre', models.IntegerField(blank=True, null=True, verbose_name='肌酐')),
                ('tt', models.FloatField(blank=True, null=True, verbose_name='凝血酶时间')),
                ('fg', models.FloatField(blank=True, null=True, verbose_name='纤维蛋白原浓度')),
                ('aptt', models.FloatField(blank=True, null=True, verbose_name='活化部分凝血活酶时间')),
                ('pt', models.FloatField(blank=True, null=True, verbose_name='凝血酶原时间')),
                ('ck', models.FloatField(blank=True, null=True, verbose_name='肌酸激酶')),
                ('ckmb', models.FloatField(blank=True, null=True, verbose_name='肌酸激酶同工酶')),
                ('cTnI', models.BinaryField(blank=True, null=True, verbose_name='肌钙蛋白I')),
                ('ct', models.BinaryField(blank=True, null=True, verbose_name='胸痛')),
                ('stt', models.BinaryField(blank=True, null=True, verbose_name='ST-T改变')),
                ('stup', models.BinaryField(blank=True, null=True, verbose_name='ST-T抬高')),
                ('std', models.BinaryField(blank=True, null=True, verbose_name='ST-T压低')),
                ('q', models.BinaryField(blank=True, null=True, verbose_name='病理性Q波')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patientbase', verbose_name='病人号')),
            ],
            options={
                'verbose_name': '患者身体信息',
                'verbose_name_plural': '患者身体信息',
            },
        ),
        migrations.AlterField(
            model_name='diagnose',
            name='medicine_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.prescribe', verbose_name='开药id'),
        ),
    ]