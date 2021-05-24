import random
from django.db import models
# Create your models here.

def random_mail():
    return str(random.randint(10000, 99999)) + "@163.com"


class Remark(models.Model):
    """
    D2 医生评价信息
    """
    remark_id = models.CharField(max_length=50,primary_key=True,verbose_name="评价id")
    diagnose_id = models.ForeignKey("patient.Diagnose",on_delete=models.CASCADE,verbose_name="诊断id")
    doctor_id = models.ForeignKey("DoctorBase",on_delete=models.CASCADE,verbose_name="医生id",default="10001") # default must?
    remark_date = models.DateField(verbose_name="评价时间")
    remark = models.TextField(verbose_name="评价内容")
    score = models.FloatField(verbose_name="评价得分")

    class Meta:
        verbose_name = verbose_name_plural = "医生评价信息"

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class Department(models.Model):
    """
    D3 科室表
    """
    dept_id = models.IntegerField(primary_key=True, verbose_name="科室号")
    doc_id = models.ForeignKey("DoctorBase",on_delete=models.CASCADE,verbose_name="科室主任",blank=True,null=True)
    # to_fields = DoctorBase.doc_name, 指定到特定的地方
    dept_name = models.CharField(max_length=50,verbose_name="科室名")

    class Meta:
        verbose_name = verbose_name_plural = "科室"

    def __str__(self):
        return '<Department:{}>'.format(self.dept_name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class Medicine(models.Model):
    """
    D4 药品价格信息
    """
    med_id = models.CharField(max_length=50,primary_key=True,verbose_name="药品id")
    med_name = models.CharField(max_length=50,verbose_name="药品名称")
    med_class = models.CharField(max_length=50,verbose_name="药品类别")
    med_price = models.FloatField(verbose_name="药品价格")
    med_stock = models.IntegerField(verbose_name="药品库存")
    initial_py = models.CharField(max_length=50, verbose_name="药品快拼")

    class Meta:
        verbose_name = verbose_name_plural = "药品价格信息"

    def __str__(self):
        return '<Doctor:{}>'.format(self.med_name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class CheckItem(models.Model):
    """
    D5 检查价格信息
    """
    check_id = models.CharField(max_length=50,primary_key=True,verbose_name="检查项目id")
    check_name = models.CharField(max_length=50,verbose_name="检查项目名字")
    check_price = models.IntegerField(verbose_name="检查价格")

    class Meta:
        verbose_name = verbose_name_plural = "检查价格"

    def __str__(self):
        return '<Check:{}>'.format(self.check_name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

class DoctorBase(models.Model):
    """
    D6 医生信息
    """
    doc_id = models.IntegerField(primary_key=True,verbose_name="医生号")
    doc_name = models.CharField(max_length=50,verbose_name="医生名字")  # 外键关联到,必须设为unique
    # dept_id = models.ForeignKey("Department",on_delete=models.CASCADE,verbose_name="科室号")
    dept_id = models.IntegerField(verbose_name="科室号")
    doc_title = models.CharField(max_length=50,verbose_name="医生职称")
    doc_mail = models.EmailField(verbose_name="医生邮箱",default=random_mail)
    password = models.CharField(max_length=50,verbose_name="密码")  # 与Patient一致

    class Meta:
        verbose_name = verbose_name_plural = "医生基本信息"

    def __str__(self):
        return '<Doctor:{}>'.format(self.doc_name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

# why 9 12 no migratoins
class Check(models.Model):
    """
    D9 检查信息
    """
    CHEST_PAIN = 1
    CHEST_NORMAL = 0
    CHEST_ITEM = (
        (CHEST_PAIN,'胸痛'),
        (CHEST_NORMAL,'正常')
    )
    report_id = models.CharField(max_length=50,primary_key=True,verbose_name="检查id")
    diagnose_id = models.ForeignKey("patient.Diagnose",on_delete=models.CASCADE,verbose_name="诊断id")
    pid = models.ForeignKey("patient.PatientBase",on_delete=models.CASCADE,verbose_name="病人号")
    check_list = models.CharField(max_length=100,verbose_name="检查内容")
    chest = models.PositiveIntegerField(default=CHEST_NORMAL,
                        choices=CHEST_ITEM,verbose_name="症状")

    class Meta:
        verbose_name = verbose_name_plural = "检查信息"

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class CheckDetail(models.Model):
    """
    D12 检查细则
    """
    detail_id = models.CharField(max_length=50,primary_key=True,verbose_name="详情id")
    diagnose_id = models.ForeignKey("patient.Diagnose",on_delete=models.CASCADE,verbose_name="诊断id")
    check_id = models.ForeignKey("CheckItem",on_delete=models.CASCADE,verbose_name="检查id")
    report_content = models.CharField(max_length=200,verbose_name="检查结果")
    check_time = models.DateField(verbose_name="检查时间")

    class Meta:
        verbose_name = verbose_name_plural = "检查详情"

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class Roster(models.Model):
    """
    D14 排班表
    """
    doc_id = models.ForeignKey("DoctorBase",on_delete=models.CASCADE,verbose_name="医生号")
    remain = models.IntegerField(default=20,verbose_name="剩余号")
    reservations = models.CharField(max_length=100,verbose_name="预约列表")

    class Meta:
        verbose_name = verbose_name_plural = "排班表"

    @classmethod
    def get_all(cls):
        return cls.objects.all()





