# Generated by Django 3.1.3 on 2021-04-28 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0012_auto_20210428_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='doc_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorbase', verbose_name='科室主任'),
        ),
    ]
