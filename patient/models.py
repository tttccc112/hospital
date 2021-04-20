from django.db import models

# Create your models here.

class Register(models.Model):
    """
    D1 挂号信息
    """
    STATUS_UNPAID = 0
    STATUS_UNDIAGNOSIS = 1
    STATUS_DIAGNOSIS = 2
    STATUS_ITEM = (
        (STATUS_UNPAID,"未缴费"),
        (STATUS_UNDIAGNOSIS,"缴费未看诊"),
        (STATUS_DIAGNOSIS,"已经看诊")
    )
    register_id = models.CharField(max_length=50,primary_key=True, verbose_name="挂号id")
    pid = models.ForeignKey("PatientBase",on_delete=models.CASCADE,verbose_name="病人号")
    doc_id = models.ForeignKey("doctor.DoctorBase",on_delete=models.CASCADE,verbose_name="医生号")
    dept_id = models.ForeignKey("doctor.Department",on_delete=models.CASCADE,verbose_name="科室号")
    register_date = models.DateField(verbose_name="挂号日期")
    status = models.PositiveIntegerField(default=STATUS_UNPAID,
                choices = STATUS_ITEM,verbose_name="当前状态")

    class Meta:
        verbose_name = verbose_name_plural = "挂号信息"

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class Fee(models.Model):
    """D7 收费流水信息"""
    fee_id = models.IntegerField(primary_key=True,verbose_name="收费单id")
    diagnose_id = models.ForeignKey("Diagnose",on_delete=models.CASCADE, verbose_name="诊断id")
    register_id = models.ForeignKey("Register", on_delete=models.CASCADE, verbose_name="挂号id")
    fee_content = models.CharField(max_length=200,verbose_name="收费明细")
    fee_total = models.FloatField(verbose_name="收费金额")
    fee_date = models.DateField(verbose_name="收费时间")

    class Meta:
        verbose_name = verbose_name_plural = "收费流水"

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class Diagnose(models.Model):
    """
    D8 诊断信息
    """
    diagnose_id = models.CharField(max_length=50,primary_key=True,verbose_name="诊断id")
    register_id = models.ForeignKey("Register",on_delete=models.CASCADE,verbose_name="挂号id")
    pid = models.ForeignKey("PatientBase",on_delete=models.CASCADE,verbose_name="病人号")
    diagnose_text = models.TextField(verbose_name="诊断信息",null=True,blank=True)
    diagnose_date = models.DateField(verbose_name="诊断时间")
    medicine_id = models.ForeignKey("doctor.Medicine",on_delete=models.CASCADE,verbose_name="开药id")
    # report_id = models.ForeignKey("doctor.Check",on_delete=models.CASCADE,verbose_name="检查id")
    fee_id = models.CharField(max_length=100,verbose_name="收费id")

    class Meta:
        verbose_name = verbose_name_plural = "诊断信息"

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class PatientBase(models.Model):
    """
    D11 患者信息
    """
    GENDER_MALE = 1
    GENDER_FEMALE = 0
    GENDER_ITEM = (
        (GENDER_MALE,'男'),
        (GENDER_FEMALE,'女')
    )


    pid = models.IntegerField(primary_key=True,verbose_name="患者号")
    pname = models.CharField(max_length=50,verbose_name="患者名字")
    pgender = models.PositiveIntegerField(default=GENDER_MALE,
                        choices=GENDER_ITEM,verbose_name="性别")
    pbirth = models.DateField(verbose_name="出生日期")
    password = models.CharField(max_length=50,verbose_name="密码")

    class Meta:
        verbose_name = verbose_name_plural = "患者基本信息"

    def __str__(self):
        return '<Patient:{}>'.format(self.pname)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @property
    def gender_show(self):
        return dict(self.GENDER_ITEM)[self.pgender]


