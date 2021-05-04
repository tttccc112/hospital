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
    diagnose_id = models.ForeignKey("Diagnose",on_delete=models.CASCADE, verbose_name="诊断id",blank=True,null=True)
    register_id = models.ForeignKey("Register", on_delete=models.CASCADE, verbose_name="挂号id",blank=True,null=True)
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
    #medicine_id = models.ForeignKey("Prescribe",on_delete=models.CASCADE,verbose_name="开药id")
    #report_id = models.ForeignKey("doctor.Check",on_delete=models.CASCADE,verbose_name="检查id",default="REPORT0")  # why default must??
    medicine_id = models.CharField(max_length=50,verbose_name="开药id")
    report_id = models.CharField(max_length=50,verbose_name="检查id",default="REPORT0")
    fee_id = models.CharField(max_length=100,verbose_name="收费id")

    class Meta:
        verbose_name = verbose_name_plural = "诊断信息"

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class Prescribe(models.Model):
    """
    D10 开药信息
    """
    prescribe_id = models.CharField(max_length=50,primary_key=True,verbose_name="开药id")
    diagnose_id = models.ForeignKey("Diagnose",on_delete=models.CASCADE,verbose_name="诊断id")
    prescribe_content = models.CharField(max_length=100,verbose_name="开药记录")
    class Meta:
        verbose_name = verbose_name_plural = "开药信息"

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


class PatientHealth(models.Model):
    """
    D13 用户身体信息
    """
    pid = models.ForeignKey("PatientBase",on_delete=models.CASCADE,verbose_name="病人号")
    pdate = models.DateField(verbose_name="入院时间")
    pgender = models.IntegerField(verbose_name="性别",blank=True,null=True)
    page = models.IntegerField(verbose_name="就诊年龄",blank=True,null=True)
    low_bp = models.IntegerField(verbose_name="舒张压",blank=True,null=True)
    high_bp = models.IntegerField(verbose_name="收缩压",blank=True,null=True)
    ast = models.IntegerField(verbose_name="天门冬氨酸氨基转移酶",blank=True,null=True)
    alat = models.IntegerField(verbose_name="丙氨酸氨基转移酶",blank=True,null=True)
    tp = models.FloatField(verbose_name="总蛋白",blank=True,null=True)
    alb = models.FloatField(verbose_name="白蛋白",blank=True,null=True)  # albumin
    glb = models.FloatField(verbose_name="球蛋白",blank=True,null=True)  # globulin
    ag = models.FloatField(verbose_name="白球蛋白比值",blank=True,null=True)
    tg = models.FloatField(verbose_name="甘油三酯",blank=True,null=True) # triglyceride
    tc = models.FloatField(verbose_name="总胆固醇",blank=True,null=True) # total cholesterol
    glc = models.FloatField(verbose_name="葡萄糖测定",blank=True,null=True) #glucose
    hdl = models.FloatField(verbose_name="高密度脂蛋白胆固醇",blank=True,null=True)  # High density liptein cholesterol
    ldl = models.FloatField(verbose_name="低密度脂蛋白胆固醇",blank=True,null=True)
    cre = models.IntegerField(verbose_name="肌酐",blank=True,null=True)  # creatinine
    tt = models.FloatField(verbose_name="凝血酶时间",blank=True,null=True)  # thrombin time
    fg = models.FloatField(verbose_name="纤维蛋白原浓度",blank=True,null=True)  # Fibrinogen
    aptt = models.FloatField(verbose_name="活化部分凝血活酶时间",blank=True,null=True)
    pt = models.FloatField(verbose_name="凝血酶原时间", blank=True, null=True) # Prothrombin time
    ck = models.FloatField(verbose_name="肌酸激酶",blank=True,null=True)  # Creatine kinase
    ckmb = models.FloatField(verbose_name="肌酸激酶同工酶",blank=True,null=True)  # creatine kinase muscle B
    cTnI = models.IntegerField(verbose_name="肌钙蛋白I",blank=True,null=True)
    ct = models.IntegerField(verbose_name="胸痛",blank=True,null=True)  # chest pain
    stt = models.IntegerField(verbose_name="ST-T改变",blank=True,null=True)
    stup = models.IntegerField(verbose_name="ST-T抬高",blank=True,null=True)
    std = models.IntegerField(verbose_name="ST-T压低",blank=True,null=True)
    q = models.IntegerField(verbose_name="病理性Q波",blank=True,null=True)

    class Meta:
        verbose_name = verbose_name_plural = "患者身体信息"

    def __str__(self):
        return '<Patient:{},{}>'.format(self.pid,self.pdate)

    @classmethod
    def get_all(cls):
        return cls.objects.all()