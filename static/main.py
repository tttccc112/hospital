import os
import sys
import time
import django
import numpy as np
from typing import List, Dict, Tuple
import datetime
import json

from Comment import CommentAnalysisSystem

nan = np.nan

os.environ['KERAS_BACKEND'] = 'tensorflow'
BASE_DIR = os.path.dirname('/Users/xie/PycharmProjects/hospital')
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from patient.models import Register, Fee, Diagnose, Prescribe, PatientBase, PatientHealth
from doctor.models import Remark, Department, Medicine, CheckItem, DoctorBase, Check, CheckDetail, Roster


class NoAttrError(Exception):
    def __init__(self, target_attr, valid_attr, process):
        self.message = '流程{}错误!输入属性/操作‘{}‘不在可行属性/操作{}中'.format(process, target_attr, valid_attr)
        print(self.message)


class PatientInfo:
    """病人信息类，负责病人信息的后台处理"""

    def __init__(self, p_id: int = None, p_name: str = None, p_gender: int = None, p_age: str = None):
        self._id = p_id  # 病人ID【int】
        self._name = p_name  # 病人姓名【str】
        self._gender = p_gender  # 病人性别【int】
        self._age = p_age  # 病人生日 【str】
        self._password = None  # 登录密码【str】
        self._diagnose_history = []  # 就诊历史，为诊断单ID【list】
        self._register_history = []  # 挂号历史，为挂号单ID【list】
        self._body_info = []  # 身体信息，为字典【dict】

    def update_info(self, attr: str, new_value):
        """
        更新患者在数据库中的信息
        :param attr: 需要更新的属性
        :param new_value: 新的值，新的body_info需要传入一个tuple（属性，值）
        :return:
        """
        valid_attr = ['gender', 'age', 'diagnose', 'register', 'body_info', 'name']
        if attr not in valid_attr:
            raise NoAttrError(attr, valid_attr, '更新患者信息')

        if attr == 'gender':
            return self._update_gender(new_gender=new_value)
        elif attr == 'name':
            return self._update_name(new_name=new_value)
        elif attr == 'age':
            return self._update_age(new_age=new_value)
        elif attr == 'diagnose':
            return self._update_diagnose_history(new_diagnose=new_value)
        elif attr == 'register':
            return self._update_register_history(new_register=new_value)
        elif attr == 'body_info':
            return self._update_body_info(info_attr=new_value[0], new_info=new_value[1])

    def update_password(self, old_password, new_password):
        """
        负责更新病人的密码
        :param old_password: 旧密码
        :param new_password: 新密码
        :return:
        """
        if old_password != self._password:
            return False
        else:
            self._update_password(new_password)

    def get_info(self, attr: str):
        """
        获取患者的某项信息
        :param attr:需要获取的属性，仅可获取valid_attr中的属性
        :return:返回需要被获取的属性
        """
        valid_attr = ['id', 'gender', 'age', 'diagnose', 'register', 'body_info', 'name']
        if attr not in valid_attr:
            raise NoAttrError(attr, valid_attr, '获取患者信息')

        if attr == 'id':
            return self._get_id()
        elif attr == 'gender':
            return self._get_gender()
        elif attr == 'name':
            return self._get_name()
        elif attr == 'age':
            return self._get_age()
        elif attr == 'diagnose':
            return self._get_diagnose_history()
        elif attr == 'register':
            return self._get_register_history()
        elif attr == 'body_info':
            return self._get_body_info()

    def load_all_from_database(self, p_id):
        """
        提供病人ID，从数据库中加载该所有信息
        :param p_id:
        :return:
        """
        self._id = p_id
        # TODO:加载所有信息，或者
        if len(PatientBase.objects.all().filter(pid=p_id)) > 0:
            patientbase = PatientBase.objects.get(pid=p_id)
            self._id = patientbase.pid
            self._name = patientbase.pname
            self._gender = patientbase.pgender
            self._age = int(datetime.date.today().year - patientbase.pbirth.year)
            self._password = patientbase.password
        if len(PatientHealth.objects.all().filter(pid=p_id)) > 0:
            patienthealth = PatientHealth.objects.get(pid=p_id)
            self._body_info = patienthealth.__dict__
        if len(Diagnose.objects.all().filter(pid=p_id)) > 0:
            diagnose = Diagnose.objects.all().filter(pid=p_id)
            for i in diagnose:
                self._diagnose_history.append(i.__dict__)
        if len(Register.objects.all().filter(pid=p_id)) > 0:
            register = Register.objects.all().filter(pid=p_id)
            for i in register:
                self._register_history.append(i.__dict__)

    def write_all_to_database(self):
        """
        将所有信息写入数据库
        :return:
        """
        if len(PatientBase.objects.all().filter(pid=self._id)) > 0:
            patientbase = PatientBase.objects.get(pid=self._id)
            patientbase.pname = self._name
            patientbase.pgender = self._gender
            patientbase.password = self._password
        else:
            PatientBase.objects.create(pid=self._id, pname=self._name, pgender=self._gender, password=self._password)

    def create_id(self, new_password):
        # TODO:创建新用户的ID与密码
        pass

    def _update_age(self, new_age):
        self._age = new_age
        self._write_info_to_database('age')

    def _update_name(self, new_name):
        self._name = new_name
        self._write_info_to_database('name')

    def _update_gender(self, new_gender):
        self._gender = new_gender
        self._write_info_to_database('gender')

    def _update_diagnose_history(self, new_diagnose):
        self._diagnose_history.append(new_diagnose)
        self._write_info_to_database('diagnose')

    def _update_register_history(self, new_register):
        self._register_history.append(new_register)
        self._write_info_to_database('register')

    def _update_body_info(self, info_attr, new_info):
        self._body_info[info_attr] = new_info
        self._write_info_to_database('body_info')

    def _update_password(self, new_password):
        self._password = new_password
        self._write_info_to_database('password')

    def _get_id(self):
        return self._id

    def _get_name(self):
        return self._name

    def _get_age(self):
        return self._age

    def _get_gender(self):
        return self._gender

    def _get_body_info(self):
        return self._body_info

    def _get_diagnose_history(self):
        return self._diagnose_history

    def _get_register_history(self):
        return self._register_history

    def _load_info_from_database(self, attr: str):
        """
        # TODO: 提供属性，从数据库中加载该属性
        从数据库中加载某项属性
        :param attr:
        :return:
        """
        if attr == 'gender':
            if len(PatientBase.objects.all().filter(pid=self._id)) > 0:
                patientbase = PatientBase.objects.get(pid=self._id)
                self._gender = patientbase.pgender
        elif attr == 'name':
            if len(PatientBase.objects.all().filter(pid=self._id)) > 0:
                patientbase = PatientBase.objects.get(pid=self._id)
                self._name = patientbase.pname
        elif attr == 'age':
            if len(PatientBase.objects.all().filter(pid=self._id)) > 0:
                patientbase = PatientBase.objects.get(pid=self._id)
                self._age = patientbase.page
        elif attr == 'diagnose':
            if len(Diagnose.objects.all().filter(pid=self._id)) > 0:
                diagnose = Diagnose.objects.all().filter(pid=self._id)
                self._diagnose_history = []
                for i in diagnose:
                    self._diagnose_history.append(i.__dict__)
        elif attr == 'register':
            if len(Register.objects.all().filter(pid=self._id)) > 0:
                register = Register.objects.all().filter(pid=self._id)
                self._register_history = []
                for i in register:
                    self._register_history.append(i.__dict__)
        elif attr == 'body_info':
            if len(PatientHealth.objects.all().filter(pid=self._id)) > 0:
                patienthealth = PatientHealth.objects.get(pid=self._id)
                self._body_info = patienthealth.__dict__

    def _load_diagnose_history(self):
        """
        加载患者历史就诊信息
        :return:
        """
        self._load_info_from_database(self, 'diagnose')

    def _load_register_history(self):
        """
        加载患者历史挂号信息
        :return:
        """
        self._load_info_from_database(self, 'register')

    def _load_body_info(self):
        """
        加载患者身体信息
        :return:
        """
        self._load_info_from_database(self, 'body_info')

    def _write_info_to_database(self, attr: str):
        """
        # TODO:将当前患者某个属性的信息写入数据库
        :param attr: 需要写入的属性
        :return:
        """
        pass


class ScheduleInfo:
    """医生排班信息类，负责医生排班信息的处理"""

    def __init__(self, doctor_id=None, date=None):
        self._doctor_id = doctor_id
        self._schedule_register = []
        self._max_schedule_number = 0
        self._date = date

    def add_register(self, register_id, date):
        """
        增加挂号信息（为医生新增挂号单）
        :param register_id: 挂号单id
        :param date: 挂号日期
        :return:
        """
        self.load_register(date=date)
        if len(self._schedule_register) < self._max_schedule_number:
            self._schedule_register.append(register_id)
            self._write_info_to_database()
        else:
            raise NoAttrError('医生排班已满', '医生排班不得超过50', '医生排班')

    def get_register_number(self):
        return len(self._schedule_register)

    def get_max_register_number(self):
        return self._max_schedule_number

    def get_register(self):
        return self._schedule_register

    def get_spare_number(self):
        """
        获取医生空余号量
        :return: 空余号量
        """
        self.load_all_from_database(doctor_id=self._doctor_id, date=self._date)
        return self._max_schedule_number - len(self._schedule_register)

    def load_register(self, date):
        """
        获取当日排班信息列表
        :param date:
        :return:
        """
        # TODO:提供日期，返回当日排班信息列表
        return self._schedule_register

    def load_all_from_database(self, doctor_id, date):
        # TODO: 从数据库加载所有信息
        # TODO: 加载当日最大排班数量！
        self._doctor_id = doctor_id
        if len(Roster.objects.filter(id=doctor_id)) > 0:
            roster = Roster.objects.get(id=doctor_id)
            self._schedule_register = json.loads(roster.reservations)
            self._max_schedule_number = roster.remain

    def _write_info_to_database(self):
        # TODO:储存当前信息至数据库
        if len(Roster.objects.filter(id=self._doctor_id)) > 0:
            roster = Roster.objects.get(id=self._doctor_id)
            roster.reservations = json.dumps(self._schedule_register)
            roster.remain = self._max_schedule_number


class DoctorInfo:
    """医生信息类，负责医生信息的处理,如改密码等"""

    def __init__(self, doctor_id=None, doctor_name=None):
        self._doctor_id = doctor_id
        self._doctor_name = doctor_name
        self._doctor_title = None
        self._department: str = None
        self._password = None

    def get_dept(self):
        return self._department

    def load_all_from_database(self, doctor_id):
        self._doctor_id = doctor_id
        doctorbase = DoctorBase.objects.get(doc_id=self._doctor_id)
        self._doctor_name = doctorbase.doc_name
        self._password = doctorbase.password
        self._department = Department.objects.get(dept_id=doctorbase.dept_id).dept_name

    def _write_info_to_database(self, attr):
        # TODO:写入信息至数据库
        if attr == 'doctor_name':
            if len(DoctorBase.objects.filter(doc_id=self._doctor_id)) > 0:
                doctorbase = DoctorBase.objects.get(doc_id=self._doctor_id)
                doctorbase.doc_name = self._doctor_name
            else:
                DoctorBase.objects.create(doc_id=self._doctor_id, doc_name=self._doctor_name)
        if attr == 'password':
            if len(DoctorBase.objects.filter(doc_id=self._doctor_id)) > 0:
                doctorbase = DoctorBase.objects.get(doc_id=self._doctor_id)
                doctorbase.password = self._password
            else:
                DoctorBase.objects.create(doc_id=self._doctor_id, password=self._password)

    def login(self, password):
        """
        医生登录认证
        TODO: 将密码转化成base64编码，或者其他形式做个简单加密
        :param password:
        :return:
        """
        if password == self._password:
            return True
        else:
            return False

    def change_password(self, old_password, new_password):
        """
        更改密码
        :param old_password: 旧密码
        :param new_password: 新密码
        :return:
        """
        if old_password == self._password:
            self._password = new_password
            self._write_info_to_database(attr='password')
            return True
        else:
            return False


class DepartmentInfo:
    """部门信息类，主要任务负责获取某科室医生空余号数"""

    def __init__(self, dept_id):
        self._dept_id = dept_id
        self._dept_name = None
        self._doctor_id_list = []

    def load_data(self, dept_id):
        if len(Department.objects.filter(dept_id=dept_id)) > 0:
            department = Department.objects.filter(dept_id=dept_id)
            for i in department:
                self._doctor_id_list.append(i.doc_id_id)

    def get_doctor_id_list(self):
        # TODO:获取科室中的医生
        pass

    def get_possible_doctor(self, date):
        """
        获取部门中出诊的医生id与剩余号
        :return: {医生ID:剩余号}
        """
        # TODO:之后可能需要转换成tuple list来排序
        return {i: ScheduleInfo(doctor_id=i, date=date).get_spare_number() for i in self._doctor_id_list}


class RegisterInfo:
    """挂号信息类，负责挂号信息的后台处理"""

    def __init__(self, patient_id=None, doctor_id=None, register_id=None):
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._register_id = register_id
        self._payment_id = None
        self._status = None

    def find_latest_id(self):
        """TODO:根据医生id与病人id从数据库找最新的挂号id"""
        regs_info = Register.objects.filter(doc_id_id=self._doctor_id, pid_id=self._patient_id).order_by(
            "register_id").reverse().first()
        self._register_id = regs_info.register_id
        return self._register_id

    def create_id(self):
        """
        创建挂号单id
        :return: 新建的挂号单id
        """
        # TODO:创建ID
        return self._register_id

    def get_id(self):
        """
        获取挂号单id
        :return: 挂号单id
        """
        return self._register_id

    def get_patient_id(self):
        """
        获取挂号单中的病人id
        :return: 病人id
        """
        return self._patient_id

    def get_doctor_id(self):
        """
        获得挂号单的医生的id
        :return: 医生id
        """
        return self._doctor_id

    def write_all_to_database(self):
        """
        将所有信息写入数据库
        :return:
        """
        # TODO:将当前信息存入数据库
        pass

    def load_all_from_database(self, register_id):
        """
        从数据库中加载所有信息
        :param register_id:挂号单id
        :return:
        """
        self._register_id = register_id
        register = Register.objects.get(register_id=register_id)
        self._patient_id = register.pid
        self.doctor_id = register.doc_id
        self.payment_id = Fee.objects.get(register_id=register_id).fee_id
        self._status = register.status
        # TODO:加载所有信息
        pass

    def add_payment(self, payment_id):
        """
        将付款单信息写入
        :param payment_id:
        :return:
        """
        self._payment_id = payment_id

    def change_status(self, new_status):
        """
        更新挂号单状态
        :param new_status:
        :return:
        """
        self._status = new_status

    def get_status(self):
        return self._status


class CheckInfo:
    """检查信息类，主要负责加载检查描述与价格等信息"""

    def __init__(self):
        self._check_id = None
        self._check_price = None
        self._check_name = None
        self._check_detail = None

    def load_all_from_database(self, check_id):
        # TODO:提供检查编号，加载检查信息
        check = CheckItem.objects.get(check_id=check_id)
        self._check_price = check.check_price
        self._check_name = check.check_name
        self._check_detail = eval(check.check_info)
        # print(self._check_price)

    def get_name(self):
        return self._check_name

    def get_price(self):
        return self._check_price

    def get_info(self):
        return self._check_detail


class MedicineInfo:
    """药品信息类，主要负责加载药品描述与价格，放到类变量medicine_money_dict中"""

    def __init__(self):
        self._medicine_id = None
        self._medicine_class = None
        self._medicine_price = None
        self._medicine_stock = None
        self._medicine_name = None
        self._medicine_fast_spell = None  # 药品快拼

    def consume_medicine(self, medicine_id, medicine_num):
        """TODO:消耗药品，提供id与消耗数量"""
        pass

    def find_fast_spell(self, fast_spell):
        medicine = Medicine.objects.get(initial_py=fast_spell)
        self.load_all_from_database(medicine_id=medicine.med_id)

    def load_all_from_database(self, medicine_id):
        """TODO:提供药品id，从数据库中加载药品所有信息"""
        medicine = Medicine.objects.get(med_id=medicine_id)
        self._medicine_id = medicine_id
        self._medicine_class = medicine.med_class
        self._medicine_stock = medicine.med_stock
        self._medicine_price = medicine.med_price
        self._medicine_name = medicine.med_name
        self._medicine_fast_spell = medicine.initial_py

    def get_price(self):
        return self._medicine_price

    def get_id(self):
        return self._medicine_id

    def get_name(self):
        return self._medicine_name


class PaymentInfo:
    """付款信息类，完成付款的后台操作"""

    def __init__(self, p_info: PatientInfo = None, detail_info: dict = None, diag_info=None,
                 regs_info: RegisterInfo = None):
        self._patient_info = p_info  # 支付患者信息
        self._money = 0  # 付款金额
        self._detail_info = detail_info  # 细节信息，为字典【收费项目：数量】
        self._diagnose_info = diag_info  # 诊断info，如果为诊断单的付款行为，则填入诊断info类
        self._register_info = regs_info  # 挂号info，如果为挂号单的付款行为，则填入挂号info类
        self._payment_status: bool = False  # 支付状态，False代表未支付，True代表已支付
        self._update_time: str = ''  # 支付单更新时间，为str
        self._payment_id = None

    def get_id(self):
        """
        获取付款id
        :return:
        """
        return self._payment_id

    def get_status(self):
        """
        获取付款状态
        :return:
        """
        return self._payment_status

    def create_payment(self, payment_type, content: dict):
        """
        创建支付单，flag指示是挂号还是诊断，content指示收费内容
        :return:
        """
        self._update_time = time.strftime("%Y-%m-%d", time.localtime())  # 创建支付单时更新创建日期
        regs_id = None
        diag_id = None
        total_fee = self.cal_money(content=content)
        new_id = Fee.objects.all().order_by("fee_id").reverse().first().fee_id + 1
        if payment_type == 'diag':
            diag_id = self._diagnose_info.get_id()
            Fee.objects.create(fee_id=new_id, diagnose_id=Diagnose.objects.get(diagnose_id=diag_id),
                               register_id=regs_id, fee_content=content,
                               fee_total=total_fee, fee_date=self._update_time)
        elif payment_type == 'regs':
            regs_id = self._register_info.get_id()
            Fee.objects.create(fee_id=new_id, diagnose_id=None, register_id=Register.objects.get(register_id=regs_id),
                               fee_content=content,
                               fee_total=total_fee, fee_date=self._update_time)
        else:
            raise NoAttrError(payment_type, ['diag', 'regs'], '创建支付单失败')
        self._payment_id = new_id
        # TODO:更改status
        # self._write_info_to_database(attr=['all'])

    def update_status(self, new_status):
        """
        更新付款状态（完成付款，将付款状态从False改为True）
        :param new_status: 新的状态
        :return:
        """
        if new_status not in [True, False]:
            raise NoAttrError(new_status, [True, False], '更新支付状态')
        else:
            self._payment_status = new_status
            if new_status:
                self._write_info_to_database(attr=['time', 'status'])
            self._update_time = time.strftime("%Y-%m-%d", time.localtime())

    def load_all_from_database(self, payment_id):
        """
        从数据库加载所有信息
        # TODO:可以完成从数据库加载部分信息的函数
        :param payment_id: 付款单ID
        :return:
        """
        self._payment_id = payment_id
        fee = Fee.objects.get(fee_id=payment_id)

        self._money = fee.fee_total
        self._detail_info = json.loads(fee.fee_content)
        self._diagnose_info = fee.diagnose_id
        self._register_info = fee.register_id
        self._update_time = fee.fee_date

    def cal_money(self, content):
        """
        计算付款金额，需要在init中填入detail_info，一份检查单仅可调用一次
        :return: 返回需要支付的金额
        """
        self._detail_info = content
        if self._money != 0:
            raise NoAttrError('金额已计算过', '不得重复计算', '计算缴费金额')
        if len(self._detail_info) == 0:
            raise NoAttrError('未输入缴费信息', '输入长度大于0', '计算缴费金额')
        for detail in self._detail_info.items():
            if detail[0][:5] == 'CHECK':
                check_info = CheckInfo()
                check_info.load_all_from_database(check_id=detail[0])
                self._money += check_info.get_price() * detail[1]
            else:
                medi_info = MedicineInfo()
                medi_info.load_all_from_database(medicine_id=detail)
                self._money += medi_info.get_price() * detail[1]
        return self._money

    def _write_info_to_database(self, attr):
        """
        # TODO:将数据写入数据库，可全部写或写某项
        :return:
        """
        pass


class DiagnoseInfo:
    """诊断信息类，对接医生系统"""

    def __init__(self, patient_id: int = None, doctor_id: int = None, register_id: int = None, diagnose_id: int = None):
        self._patient_id = patient_id
        self._doctor_id = doctor_id
        self._register_id = register_id
        self._diagnose_id = diagnose_id
        self._diagnose_info: str = ''
        self._diagnose_create_time = ''
        self._medicine_info = []
        self._check_info = []
        self._payment_info = []

    def get_diagnose_info(self):
        return self._diagnose_info

    def get_medicine_info(self):
        return self._medicine_info

    def get_register_id(self):
        return self._register_id

    def get_id(self):
        return self._diagnose_id

    def add_diagnose(self, diagnose_info: str):
        """
        增加诊断信息，为医生输入的文字
        :param diagnose_info: 医生的诊断信息
        :return:
        """
        self._diagnose_info += '\n------更新时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '------\n'
        self._diagnose_info += diagnose_info
        self._write_info_to_database('diagnose_info')

    def add_medicine(self, medicine_id):
        """
        开药。注意！输入为开药单ID！
        :param medicine_id: 开药单ID！
        :return:
        """
        # 只存储开药单编号。
        self._medicine_info.append(medicine_id)
        self._write_info_to_database('medicine_info')

    def add_check(self, check_id_ls: list):
        """
        开检查。注意！输入为检查单ID
        :param check_id: 检查单ID
        :return:
        """
        # 只存储检查单编号
        for i in check_id_ls:
            self._check_info.append(i)
        # print(self._check_info)
        self._write_info_to_database('check_info')

    def add_payment(self, payment_id):
        """
        增加付款单
        :param payment_id: 付款单编号
        :return:
        """
        self._payment_info.append(payment_id)
        self._write_info_to_database('payment_info')

    def get_id(self):
        """
        获得诊断单编号。创建ID时自动写信息入数据库
        :return: 诊断单编号
        """
        self._write_info_to_database(attr='all')
        return self._diagnose_id

    def get_patient_id(self):
        """
        获得病人编号
        :return: 病人编号
        """
        return self._patient_id

    def get_doctor_id(self):
        return self._doctor_id

    def create_id(self):
        """
        创建诊断单ID
        :return: 返回诊断单ID
        """
        self._diagnose_create_time = time.strftime("%Y-%m-%d", time.localtime())
        # TODO:创建ID函数
        return self._diagnose_id

    def load_all_from_database(self, diagnose_id):
        self._diagnose_id = diagnose_id
        # TODO:提供ID，从database加载所有信息
        diagnose = Diagnose.objects.get(diagnose_id=diagnose_id)
        self._patient_id = diagnose.pid.pid
        # print(diagnose.register_id.register_id)
        self._doctor_id = Register.objects.get(register_id=diagnose.register_id.register_id).doc_id_id
        self._register_id = diagnose.register_id.register_id
        self._diagnose_info = diagnose.diagnose_text
        self._diagnose_create_time = diagnose.diagnose_date
        self._medicine_info = eval(Prescribe.objects.get(prescribe_id=diagnose.medicine_id).prescribe_content)
        self._check_info = eval(Check.objects.get(diagnose_id=diagnose_id).check_list)
        # print(self._medicine_info)

    def _write_info_to_database(self, attr):
        possible_attr = ['check_info', 'medicine_info', 'payment_info']
        if attr == 'check_info':
            Check.objects.filter(diagnose_id=self._diagnose_id).update(check_list=json.dumps(self._check_info))
        return

    def get_check(self):
        return self._check_info


class PatientCheckInfo:
    """病人检查单的信息类，每次医生开检查就创建一个"""

    def __init__(self, diagnose_id: str, detail_id: int = None):
        """初始化时必须传入诊断单类"""
        self._diagnose_id = diagnose_id  # 诊断单id
        self._detail_id = detail_id  # 细节id
        self._check_name = None  # 检查名称
        self._check_info_id = None  # 检查名称id
        self._check_info = {}  # 检查结果，为字典, {检查属性:结果}
        self._check_status = None  # 检查状态0未缴费，1已缴费，2已检查（TODO:数据库新增状态列），由check_name对应
        self._create_time = None  # check_name: time
        self._last_update_time = None  # update_time: time
        self._diagnose_info = DiagnoseInfo()
        self._diagnose_info.load_all_from_database(diagnose_id=diagnose_id)
        self._check_id = 'REPORT' + diagnose_id.split('DIAGNOSE')[-1]
        self._check_name_id = ''

    def create_prescribe_check(self, check_info_id: str = None, check_id: str = None):
        """
        创建检查单，需要传入检查名称的id
        :param check_id: 检查名称id：CHECK1
        :param check_info_id: 检查id，D1_C1
        :return:
        """
        # TODO:检查名称列表合法性检查（不存在的检查）
        self._check_name_id = check_id
        self._create_time = time.strftime("%Y-%m-%d", time.localtime())
        self._last_update_time = time.strftime("%Y-%m-%d", time.localtime())
        self._check_info_id = check_info_id  # D1_C1形式
        check_info = CheckInfo()
        check_info.load_all_from_database(check_id=check_id)
        self._check_name = check_info.get_name()
        self._check_info = {i: nan for i in check_info.get_info()}

        if len(Check.objects.filter(report_id=self._check_id)) == 0:
            Check.objects.create(report_id=self._check_id, diagnose_id_id=self._diagnose_info.get_id(),
                                 pid_id=self._diagnose_info.get_patient_id(),
                                 check_list=json.dumps([]))

        self._write_info_to_database()
        # self._diagnose_info.add_check(self._check_id)

    def create_id(self):
        """
        创建检查单ID，首次创建时使用
        :return:
        """
        # TODO:创建ID函数
        # return self._check_id

    def update_check_info(self, attr: str, value: float):
        """
        更新检查信息
        :param attr: 检查属性
        :param value: 检查值
        :return:
        """
        if attr not in self._check_name:
            raise NoAttrError(attr, self._check_name, '更新检查信息')
        else:
            self._check_info[attr] = value
            self._last_update_time = time.strftime("%Y-%m-%d", time.localtime())
            self._write_info_to_database()
            patient_info = PatientInfo(p_id=self._diagnose_info.get_patient_id())
            patient_info.update_info(attr='body_info', new_value=(attr, value))

    def get_check_info(self, attr: str):
        """
        输入检查属性，获得检查信息
        :param attr: 检查属性
        :return:
        """
        if attr == 'all':
            return self._check_info
        elif attr not in self._check_name:
            raise NoAttrError(attr, self._check_name, '获取检查信息')
        else:
            return self._check_info[attr]

    def get_time(self):
        return self._last_update_time

    def get_status(self):
        return self._check_status

    def get_name_list(self):
        return self._check_name

    def load_all_from_database(self, check_id):
        """
        提供检查单ID，从数据库中加载所有检查详情
        :param check_id: 检查单ID
        :return:
        """
        # TODO:完成全部加载与按属性加载的功能
        if len(CheckDetail.objects.filter(detail_id=check_id)) > 0:
            # print(i)
            check_detail = CheckDetail.objects.get(detail_id=check_id)
            self._last_update_time = check_detail.check_time.strftime("%Y-%m-%d")
            # print(check_detail.report_content)
            self._check_info = eval(check_detail.report_content)
            self._check_name = self._check_info.keys()

    def _write_info_to_database(self):
        """
        # 如果CHECK无则先创建CHECK，然后插入DETAIL
        :return:
        """
        if len(CheckDetail.objects.filter(detail_id=self._check_info_id)) > 0:
            CheckDetail.objects.filter(detail_id=self._check_info_id).update(
                report_content=json.dumps(self._check_info, ensure_ascii=False),
                check_time=self._last_update_time)
        else:
            CheckDetail.objects.create(detail_id=self._check_info_id, diagnose_id_id=self._diagnose_info.get_id(),
                                       report_content=json.dumps(self._check_info, ensure_ascii=False),
                                       check_time=self._last_update_time,
                                       check_id=CheckItem.objects.get(check_id=self._check_name_id))


class PatientMedicineInfo:
    """病人开药单中的信息类，每次医生的开药操作均生成一个该信息"""

    def __init__(self, diagnose_info: DiagnoseInfo = None, patient_medicine_id: int = None,
                 medicine_info: List[tuple] = None):
        """初始化时必须传入诊断信息类"""
        self._patient_medicine_id = patient_medicine_id
        self._diagnose_info = diagnose_info  # 诊断类
        self._medicine_info = medicine_info
        self._create_time = None
        self._diagnose_id = diagnose_info.get_id()

    def create_id(self):
        # TODO:增加创建id方法
        return self._patient_medicine_id

    def create_prescribe_medicine(self, medicine_info: List[tuple]):
        """
        创建开药信息
        :param medicine_info: 开药详情列表，为{药品名:数量}构成的列表
        :return:
        """
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        val_ls = []
        for item in medicine_info:
            if item[1] != 0:
                val_ls.append(item)
        self._medicine_info = dict(val_ls)
        Prescribe.objects.filter(diagnose_id_id=self._diagnose_id).update(prescribe_content=self._medicine_info)
        # self._diagnose_info.add_medicine(medicine_id=self._patient_medicine_id)
        # self._write_info_to_database(attr='diagnose_info')

    def get_medicine_info(self):
        """
        获取开药信息
        :return:
        """
        return self._medicine_info

    def _write_info_to_database(self, attr):
        # TODO: 将当前信息写入数据库
        if attr == 'diagnose_info':
            if len(Prescribe.objects.filter(prescribe_id=self._patient_medicine_id)):
                prescibe = Prescribe.objects.get(prescibe_id=self._patient_medicine_id)
                prescibe.diagnose_id_id = self._diagnose_id
            else:
                Prescribe.objects.create(prescibe_id=self._patient_medicine_id,
                                         diagnose_id_id=self._diagnose_id)
        if attr == 'medicine_info':
            if len(Prescribe.objects.filter(prescribe_id=self._patient_medicine_id)):
                prescibe = Prescribe.objects.get(prescribe_id=self._patient_medicine_id)
                prescibe.prescribe_content = json.dumps(self._medicine_info)
            else:
                Prescribe.objects.create(prescribe_id=self._patient_medicine_id,
                                         prescribe_content=json.dumps(self._medicine_info))

    def load_all_from_database(self, diagnose_id):
        self._diagnose_id = diagnose_id
        # self._patient_medicine_id = patient_medicine_id
        if len(Prescribe.objects.filter(diagnose_id_id=diagnose_id)):
            prescibe = Prescribe.objects.get(diagnose_id_id=diagnose_id)
            # self._diagnose_info = Diagnose.objects.get(diagnose_id=prescibe.diagnose_id_id)
            self._medicine_info = json.loads(prescibe.prescribe_content)


class CommentInfo:
    """评论信息类，为病人的评论信息，默认一次诊断仅做一次评论"""

    def __init__(self, diagnose_id, comment_id=None):
        """初始化时必须传入诊断单信息"""
        self._diagnose_id = diagnose_id
        self._comment_info = None
        self._create_time = None
        self._comment_trend = None
        self._doctor_id = None
        self._comment_id = comment_id

    def create_id(self):
        """
        创建评论ID
        :return:
        """
        # TODO: 创建id
        pass

    def make_comment(self, comment_info: str):
        """
        病人做评价
        :param comment_info: 病人评价
        :return:
        """
        self._comment_info = comment_info
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._cal_comment_trend()
        diagnose_info = DiagnoseInfo()
        diagnose_info.load_all_from_database(diagnose_id=self._diagnose_id)
        self._doctor_id = diagnose_info.get_doctor_id()  # 获取医生id，以便后续查找
        self._write_info_to_database('all')

    def _cal_comment_trend(self):
        self._comment_trend = CommentAnalysisSystem.single_predict(self._comment_info)
        pass

    def _write_info_to_database(self, attr='all'):
        # TODO: 将当前信息写入数据库
        Remark.objects.create(remark_id=self._comment_id, scores=self._comment_trend,
                              remark_date=self._create_time, diagnose_id=self._diagnose_id,
                              remark=self._comment_info)


class PaymentSystem:
    def __init__(self):
        pass

    @staticmethod
    def create_payment_info(p_id: int, detail_info: dict, diag_id=None, regs_id=None):
        """
        创建支付信息，传入病人id，支付详情与诊断id/挂号id
        :param p_id: 病人id
        :param detail_info:付款细节
        :param diag_id: 诊断id
        :param regs_id: 挂号id
        :return:
        """
        p_info = PatientInfo()
        p_info.load_all_from_database(p_id=p_id)
        if diag_id is not None and regs_id is not None:
            raise NoAttrError('同时输入注册单与挂号单', '仅可输入一种单据', '创建支付单')
        elif diag_id is not None:
            diag_info = DiagnoseInfo()
            diag_info.load_all_from_database(diagnose_id=diag_id)
            payment_info = PaymentInfo(p_info, detail_info, diag_info=diag_info, regs_info=None)
            payment_info.create_payment(payment_type='diag', content=detail_info)
            diag_info.add_payment(payment_info.get_id())
        elif regs_id is not None:
            regs_info = RegisterInfo()
            regs_info.load_all_from_database(register_id=regs_id)
            payment_info = PaymentInfo(p_info, detail_info, diag_info=None, regs_info=regs_info)
            payment_info.create_payment(payment_type='regs', content=detail_info)
        return payment_info.get_id()

    @staticmethod
    def load_payment_info(payment_id):
        """
        加载支付信息
        :param payment_id:支付单id
        :return:
        """
        payment_info = PaymentInfo()
        payment_info.load_all_from_database(payment_id)
        return payment_info

    @staticmethod
    def make_payment(payment_id):
        """
        付款，提供付款单id
        :param payment_id: 支付单id
        :return:
        """
        payment_info = PaymentSystem.load_payment_info(payment_id)
        payment_info.update_status(True)
        return True


class PatientSystem:
    """病人系统"""

    def __init__(self, patient_id: int = None):
        """除注册外，其他功能均需初始化时提供病人id"""
        self._patient_id = patient_id

    @staticmethod
    def load_patient_info(patient_id):
        """
        加载病人信息，需要提供病人id，返回病人信息类
        :return:
        """
        p_info = PatientInfo(p_id=patient_id)
        p_info.load_all_from_database(p_id=patient_id)
        p_dict = []
        p_dict['']
        return p_info

    @staticmethod
    def load_history_diagnose_id(patient_id):
        # TODO: 加载历史诊断单信息，按时间顺序由最近至最远排列，返回id列表
        diag_his = Diagnose.objects.filter(pid=patient_id).order_by('diagnose_date').reverse()
        return_ls = []
        for i in diag_his:
            return_ls.append(i.diagnose_id)
        return return_ls

    @staticmethod
    def load_body_info(patient_id):
        patient_info = list(PatientHealth.objects.filter(pid_id=patient_id).order_by('pdate').values())
        info_ls = list(patient_info[0].keys())
        remove_ls = ['id', 'pdate', 'pid_id']
        for word in remove_ls:
            info_ls.remove(word)
        info_dict = {i: '' for i in info_ls}
        for item in patient_info:
            for attr in info_ls:
                if item[attr] is not None:
                    info_dict[attr] = item[attr]
        return info_dict

    @staticmethod
    def load_history_check_id(patient_id):
        # TODO: 加载历史检查单信息，按时间顺序由最近至最远排列，返回id列表
        return []

    @staticmethod
    def registration(name, age, gender, password):
        """
        注册用户，需输入姓名，年龄，性别与密码。返回病人信息类
        :param name: 姓名
        :param age: 年龄
        :param gender: 性别
        :param password: 密码
        :return:
        """
        p_info = PatientInfo(p_name=name, p_gender=gender, p_age=age)
        p_info.create_id(new_password=password)
        p_info.write_all_to_database()
        return p_info

    @staticmethod
    def update_info(patient_id, attr, value):
        """
        更新个人信息
        :param patient_id: 病人id
        :param attr: 属性
        :param value: 值
        :return:
        """
        p_info = PatientInfo(p_id=patient_id)
        p_info.load_all_from_database(p_id=patient_id)
        p_info.update_info(attr=attr, new_value=value)

    def update_password(self, old_password, new_password):
        """
        更新密码
        :param old_password: 旧密码
        :param new_password: 新密码
        :return:
        """
        if self._patient_id is None:
            raise NoAttrError('无病人id', '需提供病人id', '加载病人信息')
        p_info = PatientInfo(p_id=self._patient_id)
        p_info.update_password(old_password=old_password, new_password=new_password)


class MedicineSystem:
    """药品系统"""

    def __init__(self):
        pass

    @staticmethod
    def add_medicine(medicine_id, add_num):
        # TODO:增加药品库存，可能没用，可删
        pass

    @staticmethod
    def fast_find_medicine(fast_spell):
        medicine_info = MedicineInfo()
        medicine_info.find_fast_spell(fast_spell=fast_spell)
        return [medicine_info.get_id(), medicine_info.get_name()]

    @staticmethod
    def prescribe_medicine(diagnose_id, medicine_info_list: List[tuple]):
        """
        医生开药，提供药品信息列表，为[(药品名称,数量)]
        :param diagnose_id: 诊断单id
        :param medicine_info_list: 药品信息列表
        :return:
        """
        diagnose_info = DiagnoseInfo()
        diagnose_info.load_all_from_database(diagnose_id=diagnose_id)
        medicine_info = PatientMedicineInfo(diagnose_info=diagnose_info)
        medicine_info.create_id()
        medicine_info.create_prescribe_medicine(medicine_info_list)
        payment_info = PaymentSystem()
        payment_info.create_payment_info(p_id=diagnose_info.get_patient_id(), detail_info=dict(medicine_info_list),
                                         diag_id=diagnose_id)

    @staticmethod
    def consume_medicine(medicine_info_id):
        # TODO:减少数据库中的药品库存（在用户点击取药后减少库存）
        pass


class CheckSystem:
    def __init__(self):
        pass

    @staticmethod
    def prescribe_check(diagnose_id, check_name_list: list):
        """
        医生开检查，提供检查名称列表
        :param diagnose_id: 诊断单id
        :param check_name_list:检查名称列表
        :return:
        """
        # 医生开检查
        diagnose_info = DiagnoseInfo()
        diagnose_info.load_all_from_database(diagnose_id=diagnose_id)
        check_info = PatientCheckInfo(diagnose_info=diagnose_info)
        check_info.create_prescribe_check(check_name=check_name_list)
        payment_info = PaymentSystem()
        payment_info.create_payment_info(p_id=diagnose_info.get_patient_id(),
                                         detail_info={i: 1 for i in check_name_list},
                                         diag_id=diagnose_id)

    @staticmethod
    def update_check_info(check_id, attr: str, value: float):
        """
        病人做检查
        :param check_id: 检查单id
        :param attr: 检查项目
        :param value: 检查值
        :return:
        """
        check_info = PatientCheckInfo()
        check_info.load_all_from_database(check_id=check_id)
        check_info.update_check_info(attr=attr, value=value)

    @staticmethod
    def get_possible_check():
        """返回所有可以开的检查 字典列表：【{ID，名称}，{}】"""
        check = CheckItem.objects.all().values()
        return_ls = []
        for item in check:
            return_ls.append({'ID': item['check_id'], 'name': item['check_name']})
        # print(return_ls)
        return return_ls


class CommentSystem:
    """评论系统，用户对医生做出评价"""

    def __init__(self):
        pass

    @staticmethod
    def make_comment(diagnose_id, comment_info):
        comment = CommentInfo(diagnose_id=diagnose_id)
        comment.make_comment(comment_info=comment_info)

    @staticmethod
    def find_all_comment(doctor_id):
        """近期评价，【{1，日期，内容，星级}，{2，日期，内容，星级}，{3，日期，内容，星级}】按日期降序排列"""
        comment = Remark.objects.filter(doctor_id=doctor_id).order_by("remark_date").reverse().values()
        return_ls = []
        count = 1
        for item in comment:
            return_ls.append({'index': count, 'date': item['remark_date'], 'comment': item['remark'],
                              'star': int(item['score'] * 5 + 1)})
        return return_ls

    @staticmethod
    def find_comment_star(doctor_id):
        """不同星级的评价数，列表【一星，二星，三星，四星，五星】"""
        comment = Remark.objects.filter(doctor_id=doctor_id).values()
        comment_ls = [0, 0, 0, 0, 0]
        for item in comment:
            if item['score'] > 0.8:
                comment_ls[4] += 1
            elif item['score'] > 0.6:
                comment_ls[3] += 1
            elif item['score'] > 0.4:
                comment_ls[2] += 1
            elif item['score'] > 0.2:
                comment_ls[1] += 1
            else:
                comment_ls[0] += 1
        return comment_ls

    @staticmethod
    def find_comment_evaluate(doctor_id):
        comment = Remark.objects.filter(doctor_id=doctor_id).values()
        comment_ls = [0, 0]
        for item in comment:
            if item['score'] > 0.5:
                comment_ls[0] += 1
            else:
                comment_ls[1] += 1
        return comment_ls


class DiagnoseSystem:
    """诊断系统，提供医生诊断的所有功能，可被视为医生系统"""

    def __init__(self):
        pass

    @staticmethod
    def create_id(register_id):
        """
        创建诊断单ID。提供挂号单ID，返回诊断单ID
        :return: 返回诊断单ID
        """
        regs_info = RegisterInfo()
        regs_info.load_all_from_database(register_id=register_id)
        diag_info = DiagnoseInfo(patient_id=regs_info.get_patient_id(),
                                 register_id=register_id,
                                 doctor_id=regs_info.get_doctor_id())
        return diag_info.create_id()

    @staticmethod
    def create_check(diagnose_id, check_info: list):
        """
        创建检查单
        :param diagnose_id: 诊断单ID
        :param check_info: 检查明细，为列表
        :return:
        """
        diag_num = diagnose_id.split('DIAGNOSE')[-1]
        new_check_info_list = ['D' + diag_num + '_C' + i.split('CHECK')[-1] for i in check_info]
        # print(new_check_info_list)
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)
        diag_info.add_check(check_id_ls=new_check_info_list)
        for i in range(len(new_check_info_list)):
            patient_check_info = PatientCheckInfo(diagnose_id=diagnose_id)
            patient_check_info.create_prescribe_check(check_info_id=new_check_info_list[i], check_id=check_info[i])

        payment_info = PaymentSystem()
        payment_id = payment_info.create_payment_info(p_id=diag_info.get_patient_id(),
                                                      detail_info={i: 1 for i in check_info},
                                                      diag_id=diag_info.get_id())

        diag_info.add_payment(payment_id)

    @staticmethod
    def create_medicine(diagnose_id, medicine_info: List[tuple]):
        """将要开的药品存入数据库：【（ID，数量），】，如果数量检测为0，在原数据库中删除该药品"""
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)

        patient_medicine_info = PatientMedicineInfo(diagnose_info=diag_info)
        patient_medicine_info.create_prescribe_medicine(medicine_info=medicine_info)

        # payment_info = PaymentSystem()
        # payment_id = payment_info.create_payment_info(p_id=diag_info.get_patient_id(),
        #                                               detail_info=dict(medicine_info),
        #                                               diag_id=diag_info.get_id())
        #
        # diag_info.add_payment(payment_id)

    @staticmethod
    def create_diagnose(diagnose_id, diagnose_info):
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)
        diag_info.add_diagnose(diagnose_info)


class RegisterSystem:
    """挂号系统"""

    def __init__(self, patient_id=None, doctor_id=None, regs_id=None, date=None):
        self._patient_id = patient_id
        self._regs_id = regs_id
        self._doctor_id = doctor_id
        self._date = date

    @staticmethod
    def get_possible_doctor(dept_id, date):
        """
        查找剩余号源
        :param date: 查找日期
        :param dept_id: 查找部门
        :return:
        """
        return DepartmentInfo(dept_id=dept_id).get_possible_doctor(date=date)

    @staticmethod
    def make_register(patient_id, doctor_id, date):
        register_info = RegisterInfo(patient_id=patient_id, doctor_id=doctor_id)
        register_info.create_id()
        register_info.write_all_to_database()

        payment_info = PaymentSystem()
        payment_info.create_payment_info(p_id=patient_id, detail_info={'register': 1}, regs_id=register_info.get_id())
        # TODO:detail_info后续可能要修改

        schedule_info = ScheduleInfo(doctor_id=doctor_id, date=date)
        schedule_info.add_register(register_id=register_info.get_id(), date=date)

    @staticmethod
    def find_latest_register_info(doctor_id, patient_id):
        """TODO:根据医生id与病人id查找最新的挂号id，还有病人详情"""
        regs_info = RegisterInfo(doctor_id=doctor_id, patient_id=patient_id)
        patient_info = PatientInfo()
        patient_info.load_all_from_database(p_id=patient_id)
        regs_detail_dict = {'regs_id': regs_info.find_latest_id(),
                            'name': patient_info.get_info('name'),
                            'gender': patient_info.get_info('gender'),
                            'age': patient_info.get_info('age')}
        return regs_detail_dict


class DoctorSystem:
    """医生系统"""

    @staticmethod
    def get_doctor_patient_num(doctor_id, date):
        """某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】"""
        schedule_info = ScheduleInfo(doctor_id=doctor_id)
        schedule_info.load_all_from_database(doctor_id=doctor_id, date=date)
        return [schedule_info.get_register_number(),
                schedule_info.get_max_register_number() - schedule_info.get_register_number()]

    @staticmethod
    def get_doctor_patient(doctor_id, date):
        """某医生ID下的已看病人，字典形式：{ID：【姓名，年龄】}"""
        schedule_info = ScheduleInfo(doctor_id=doctor_id)
        schedule_info.load_all_from_database(doctor_id=doctor_id, date=date)
        register_list = schedule_info.get_register()
        patient_dict = {}
        for register in register_list:
            regs_info = RegisterInfo()
            regs_info.load_all_from_database(register_id=register)
            if regs_info.get_status() == 2:
                patient_info = PatientInfo()
                patient_info.load_all_from_database(p_id=regs_info.get_patient_id())
                patient_dict['id'] = patient_info.get_info('id')
                patient_dict['name'] = patient_info.get_info('name')
                patient_dict['age'] = patient_info.get_info('age')
        return patient_dict

    @staticmethod
    def get_doctor_comment(doctor_id):
        """根据医生ID读取评价评分（医生评分用评分均值，好评率为大于50数）"""
        """3、当前医生ID下的评级和好评比率，【星级数，好评比率】"""
        star_ls = SearchSystem.find_doctor_star(doctor_id)
        count_ls = SearchSystem.find_doctor_evaluate(doctor_id)
        star_sum = 0
        for i in range(len(star_ls)):
            star_sum += star_ls[i] * (i + 1)
        return [star_sum / sum(star_ls), count_ls[0] / sum(count_ls)]


class SearchSystem:
    """查询系统，完成与查询有关的所有函数"""

    @staticmethod
    def find_possible_check():
        """TODO:从数据库获取所有检查信息，可以开具的检查（静态固定的6种检查）：字典列表：【{ID，名称}，{}】"""
        check = CheckSystem()
        check_info = check.get_possible_check()
        return check_info

    @staticmethod
    def find_check_info(check_id):
        return_list = []
        """TODO:完成检查名称列表的加载"""
        check_name_dict = {}
        """提供该检查id下的详情，根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】"""
        check_info = PatientCheckInfo()
        check_info.load_all_from_database(check_id=check_id)
        check = CheckItem.objects.get(check_id='CHECK' + str(check_id.split('_')[-1][1:]))
        name = check.check_name
        check_time = check_info.get_time()
        attr_dict = check_info.get_check_info('all')
        return_list.append([name, check_time, list(attr_dict.keys()), list(attr_dict.values())])
        return return_list

    @staticmethod
    def find_diagnose_check(diagnose_id):
        """已开检查：字典列表，【{ID，名称，时间，状态（三种：未缴费、已缴费、已结束）}，{}，{}】"""
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)
        check_info_ls = diag_info.get_check()
        check_dict_ls = []
        for check in check_info_ls:
            check_info_id = 'CHECK' + str(check.split('_')[-1][1:])
            # print(check_info_id, check)
            check_info = CheckInfo()
            patient_check_info = PatientCheckInfo(diagnose_id=diagnose_id)
            check_info.load_all_from_database(check_id=check_info_id)
            patient_check_info.load_all_from_database(check_id=check)
            check_dict = {'id': check, 'name': check_info.get_name(),
                          'time': patient_check_info.get_time(), 'status': patient_check_info.get_status()}
            # print(check_dict)
            check_dict_ls.append(check_dict)
        return check_dict_ls

    @staticmethod
    def find_history_diagnose_info(patient_id):
        """history网页独有，当前患者ID下的所有历史诊断ID：
        # 1、字典列表：【{诊断ID，科室，诊断}，{}，{}】"""
        history_diagid_ls = PatientSystem().load_history_diagnose_id(patient_id)
        return_ls = []
        for diag_id in history_diagid_ls:
            diag_info = DiagnoseInfo()
            diag_info.load_all_from_database(diagnose_id=diag_id)
            doctor_info = DoctorInfo()
            doctor_info.load_all_from_database(doctor_id=diag_info.get_doctor_id())
            diag_info_str = diag_info.get_diagnose_info()
            return_ls.append({'diagnose_id': diag_id,
                              'dept': doctor_info.get_dept(),
                              'diagnose_info': diag_info_str})
        return return_ls

    @staticmethod
    def find_basic_diagnose_info(diagnose_id):
        """1、基本信息：字典形式{姓名，性别，生日，挂号ID}"""
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)
        patient_info = PatientInfo()
        patient_info.load_all_from_database(p_id=diag_info.get_patient_id())
        return {'name': patient_info.get_info(attr='name'),
                'gender': patient_info.get_info(attr='gender'),
                'age': patient_info.get_info(attr='age'),
                'register_id': diag_info.get_register_id()}

    @staticmethod
    def find_diagnose_prescribe(diagnose_id):
        """返回诊断文本信息"""
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id)
        return diag_info.get_diagnose_info()

    @staticmethod
    def find_diagnose_medicine(diagnose_id):
        """已开药品：字典列表，【{ID，名称，数量}，{}，{}】"""
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id)
        medicine_info_dict = diag_info.get_medicine_info()
        # print(medicine_info_dict)
        return_ls = []
        for medicine_id, amount in medicine_info_dict.items():
            medi_info = MedicineInfo()
            medi_info.load_all_from_database(medicine_id=medicine_id)
            return_ls.append({'ID': medicine_id, 'name': medi_info.get_name(), 'amount': amount})
        return return_ls

    @staticmethod
    def find_history_check_info(patient_id):
        """# 1、字典列表：【{检查ID，日期，名称，诊断}，{}，{}】"""
        history_diag_ls = PatientSystem().load_history_diagnose_id(patient_id)
        return_ls = []
        for diag_id in history_diag_ls:
            diag_info = DiagnoseInfo()
            diag_info.load_all_from_database(diagnose_id=diag_id)
            check_info = SearchSystem.find_diagnose_check(diagnose_id=diag_id)
            for check in check_info:
                return_ls.append({'check_id': check['id'],
                                  'date': check['time'],
                                  'name': check['name']})
        return return_ls

    @staticmethod
    def find_doctor_star(doctor_id):
        """不同星级的评价数，列表【一星，二星，三星，四星，五星】"""
        return CommentSystem.find_comment_star(doctor_id=doctor_id)

    @staticmethod
    def find_doctor_evaluate(doctor_id):
        """[好评数，差评数]"""
        return CommentSystem.find_comment_evaluate(doctor_id=doctor_id)

    @staticmethod
    def find_doctor_comment(doctor_id):
        """近期评价，【{1，日期，内容，星级}，{2，日期，内容，星级}，{3，日期，内容，星级}】按日期降序排列"""
        return CommentSystem.find_all_comment(doctor_id=doctor_id)

    @staticmethod
    def find_patient_body_info(patient_id):
        return PatientSystem.load_body_info(patient_id=patient_id)


class AIDiagnoseSystem:
    """智能诊断系统"""
    pass


print(RegisterSystem.find_latest_register_info(doctor_id=10248, patient_id=2110))
# print(SearchSystem.find_diagnose_check(diagnose_id='DIAGNOSE1'))
# print(SearchSystem.find_possible_check())
# print(SearchSystem.find_diagnose_prescribe(diagnose_id='DIAGNOSE1'))
# print(SearchSystem.find_diagnose_medicine(diagnose_id='DIAGNOSE1'))
# DiagnoseSystem.create_check(diagnose_id='DIAGNOSE1', check_info=['CHECK1']) 【增加部分待完成】
# print(SearchSystem.find_check_info(check_id='D1_C9'))
# print(SearchSystem.find_history_diagnose_info(patient_id=2110))
# print(SearchSystem.find_basic_diagnose_info(diagnose_id='DIAGNOSE1'))
# print(SearchSystem.find_history_check_info(patient_id=2110))
# print(MedicineSystem.fast_find_medicine('aspl'))
# print(SearchSystem.find_doctor_star(doctor_id=10001))
# print(SearchSystem.find_doctor_evaluate(doctor_id=10001))
# print(SearchSystem.find_doctor_comment(doctor_id=10001))
# print(SearchSystem.find_patient_body_info(patient_id=19794))
# print(DoctorSystem.get_doctor_comment(doctor_id=10001))
# DiagnoseSystem.create_check(diagnose_id="DIAGNOSE1", check_info=['CHECK1'])
# print(SearchSystem.find_diagnose_check(diagnose_id='DIAGNOSE1'))
DiagnoseSystem.create_medicine(diagnose_id="DIAGNOSE1", medicine_info=[('C41', 0), ('C33', 2)])

# TODO:有些类之间传类变量感觉冗余，能传id尽量传id。
# TODO:所有List[tuple]类型可直接改成dict，但会失去顺序，需讨论
# TODO:全部数据库连接工作未完成
# TODO:评论未完成
# TODO:某些状态检查支付没有做，要保证按顺序调用函数

# CommentAnalysisSystem().single_predict('医术高明，妙手回春')
# CommentAnalysisSystem().single_predict('垃圾医生')
# CommentAnalysisSystem().multiple_predict(['医术高明，妙手回春', '垃圾医生'])


# 所有网页共用：
# 1、某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】 -> DoctorSystem.get_doctor_patient_num(doctor_id, date)
# 2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄} -> DoctorSystem.get_doctor_patient(doctor_id, date)
# 3、当前医生ID下的评级和好评比率，【星级数，好评比率】-> DoctorSystem.get_doctor_comment(doctor_id) 【已完成】

# index页面独有（根据医生doc和患者pat获得的“最新”“诊断ID”下的信息：
# 1、基本信息：字典形式{姓名，性别，生日，挂号ID} -> RegisterSystem.find_latest_register_info(doctor_id, patient_id) 【已完成】
# 2、已开检查：字典列表，【{ID，名称，时间，状态（三种：未缴费、已缴费、已结束）}，{}，{}】 -> SearchSystem.find_diagnose_check(diagnose_id)【已完成，check_id待更改】
# 3、可以开具的检查（静态固定的6种检查）：字典列表：【{ID，名称}，{}】-> CheckSystem.find_check 【已完成】
# 4、诊断内容：文本 -> SearchSystem.find_diagnose_prescribe(diagnose_id) 获得诊断信息 【已完成】
# 5、已开药品：字典列表，【{ID，名称，数量}，{}，{}】 SearchSystem.find_diagnose_medicine(diagnose_id) 【已完成】

# 将要开的检查存入数据库，得到一个ID列表，写入当前诊断ID或者挂号ID下的数据库中（还会自动生成收费单） -> DiagnoseSystem.create_check(diagnose_id, check_info: list) 【已完成】
# 将要开的药品存入数据库：【（ID，数量），】，如果数量检测为0，在原数据库中删除该药品（不会自动收费，需要手动完成）
# -> DiagnoseSystem.create_medicine(diagnose_id, medicine_info: List[tuple]) 【已完成】
# 根据所得简写检索得到药品列表[id，名称]，改写message后发送给前端 -> MedicineSystem.fast_find_medicine(药品简写)【已完成】
# 更新诊断数据库
# 提供该检查id下的详情，根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】-> SearchSystem.find_check_info(check_id)【已完成】

# history网页独有，当前患者ID下的所有历史诊断ID：【有下面的了，不需要这个】
# 1、字典列表：【{诊断ID，科室，诊断}，{}，{}】-> SearchSystem.find_diagnose_info【已完成】

# check网页独有，当前患者ID下的所有历史检查ID： id从字典列表里面取
# 1、字典列表：【{检查ID，日期，名称，诊断}，{}，{}】
# 提供该检查id下的详情
# 根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】 SearchSystem.find_check_info

# decide网页独有：
# 1、字典，{各属性}   （由于属性太多，请给每个属性都取个名字，然后把值传给我，没有就空字符串）SearchSystem.find_patient_body_info(patient_id) 【已完成】

# arrange网页独有,当前医生doc下的本日病人：
# 1、字典列表，【{病人ID，姓名，年龄}，{}，{}】
# 2、列表，周一到周五的安排看诊数【1,2,3,4,5,6,7】

# evaluation网页独有,当前医生doc下评价：
# 1、不同星级的评价数，列表【一星，二星，三星，四星，五星】-> SearchSystem.find_doctor_star(doctor_id) 【已完成】
# 2、好评数、差评数，【好评数，差评数】-> SearchSystem.find_doctor_evaluate(doctor_id) 【已完成】
# 近期评价，【{1，日期，内容，星级}，{2，日期，内容，星级}，{3，日期，内容，星级}】按时间排序并根据顺序给出ID SearchSystem.find_doctor_comment 【已完成】
