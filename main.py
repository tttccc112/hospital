import os
import pickle
import string
import sys
import time
import jieba
import django
import numpy as np
from typing import List, Dict, Tuple
from keras.preprocessing import sequence
from keras.engine.saving import load_model

# from patient.models import Register, Fee, Diagnose, Prescribe, PatientBase, PatientHealth

BASE_DIR = os.path.dirname('/Users/xie/PycharmProjects/hospital')
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()


class NoAttrError(Exception):
    def __init__(self, target_attr, valid_attr, process):
        self.message = '流程{}错误!输入属性/操作‘{}‘不在可行属性/操作{}中'.format(process, target_attr, valid_attr)
        print(self.message)


class PatientInfo:
    """病人信息类，负责病人信息的后台处理"""

    def __init__(self, p_id: int = None, p_name: str = None, p_gender: str = None, p_age: int = None):
        self._id = p_id  # 病人ID【int】
        self._name = p_name  # 病人姓名【str】
        self._gender = p_gender  # 病人性别【str】
        self._age = p_age  # 病人年龄【int】
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
        pass

    def write_all_to_database(self):
        """
        将所有信息写入数据库
        :return:
        """
        pass

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
        pass

    def _load_diagnose_history(self):
        """
        加载患者历史就诊信息
        :return:
        """
        pass

    def _load_register_history(self):
        """
        加载患者历史挂号信息
        :return:
        """
        pass

    def _load_body_info(self):
        """
        加载患者身体信息
        :return:
        """
        pass

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
        pass

    def _write_info_to_database(self):
        # TODO:储存当前信息至数据库
        pass


class DoctorInfo:
    """医生信息类，负责医生信息的处理,如改密码等"""

    def __init__(self, doctor_id=None, doctor_name=None):
        self._doctor_id = doctor_id
        self._doctor_name = doctor_name
        self._password = None

    def load_all_from_database(self):
        # TODO:从数据库加载所有信息
        pass

    def _write_info_to_database(self, attr):
        # TODO:写入信息至数据库
        pass

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
        self._doctor_id_list = []

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
        # TODO:加载所有信息
        pass

    def add_payment(self, payment_id):
        """
        将付款单信息写入
        :param payment_id:
        :return:
        """
        self._payment_id = payment_id


class CheckInfo:
    """检查信息类，主要负责加载检查描述与价格，放到类变量check_money_dict中"""
    # TODO:未完成
    check_money_dict = {}

    def __init__(self):
        pass


class MedicineInfo:
    """药品信息类，主要负责加载药品描述与价格，放到类变量medicine_money_dict中"""
    # TODO:未完成
    medicine_money_dict = {}

    def __init__(self):
        pass


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

    def create_id(self):
        """
        创建支付单ID
        设想为从数据库找最大ID，然后目前ID为最大ID+1
        :return: 返回新支付单的ID
        """
        # TODO:创建支付单ID
        self._update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建支付单时更新创建日期
        return self._payment_id

    def create_payment(self):
        """
        创建支付单，在调用前需先调用create_id
        :return:
        """
        self._write_info_to_database(attr=['all'])

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
            self._update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def load_all_from_database(self, payment_id):
        """
        从数据库加载所有信息
        # TODO:可以完成从数据库加载部分信息的函数
        :param payment_id: 付款单ID
        :return:
        """
        self._payment_id = payment_id
        pass

    def cal_money(self):
        """
        计算付款金额，需要在init中填入detail_info，一份检查单仅可调用一次
        :return: 返回需要支付的金额
        """
        if self._money != 0:
            raise NoAttrError('金额已计算过', '不得重复计算', '计算缴费金额')
        if len(self._detail_info) == 0:
            raise NoAttrError('未输入缴费信息', '输入长度大于0', '计算缴费金额')
        money_dict = dict(list(CheckInfo.check_money_dict.items()) + list(MedicineInfo.medicine_money_dict.items()))
        for detail in self._detail_info.items():
            if detail[0] not in money_dict.keys():
                raise NoAttrError(detail[0], money_dict.keys(), '计算缴费金额')
            else:
                self._money += money_dict[detail[0]] * detail[1]
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

    def add_check(self, check_id):
        """
        开检查。注意！输入为检查单ID
        :param check_id: 检查单ID
        :return:
        """
        # 只存储检查单编号
        self._check_info.append(check_id)
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
        self._diagnose_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # TODO:创建ID函数
        return self._diagnose_id

    def load_all_from_database(self, diagnose_id):
        self._diagnose_id = diagnose_id
        # TODO:提供ID，从database加载所有信息
        pass

    def _write_info_to_database(self, attr):
        # TODO:将信息写入数据库（可做分属性写入）
        pass


class PatientCheckInfo:
    """病人检查单的信息类，每次医生开检查就创建一个"""

    def __init__(self, diagnose_info: DiagnoseInfo = None, check_id: int = None):
        """初始化时必须传入诊断单类"""
        self._diagnose_info = diagnose_info  # 诊断类
        self._check_id = check_id  # 检查单ID
        self._check_name = []  # 检查名称列表，为需要做的检查
        self._check_info = {}  # 检查结果，为字典{检查名:结果}
        self._create_time = None
        self._last_update_time = None

    def create_prescribe_check(self, check_name: list = None):
        """
        创建检查单，需要传入检查名称的列表
        :param check_name: 检查名称的列表
        :return:
        """
        # TODO:检查名称列表合法性检查（不存在的检查）
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._check_name = check_name
        self._check_info = {i: None for i in check_name}
        self._write_info_to_database()
        self._diagnose_info.add_check(self._check_id)

    def create_id(self):
        """
        创建检查单ID，首次创建时使用
        :return:
        """
        # TODO:创建ID函数
        return self._check_id

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
            self._last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self._write_info_to_database()
            patient_info = PatientInfo(p_id=self._diagnose_info.get_patient_id())
            patient_info.update_info(attr='body_info', new_value=(attr, value))

    def get_check_info(self, attr: str):
        """
        输入检查属性，获得检查信息
        :param attr: 检查属性
        :return:
        """
        if attr not in self._check_name:
            raise NoAttrError(attr, self._check_name, '更新检查信息')
        else:
            return self._check_info[attr]

    def load_all_from_database(self, check_id):
        """
        提供检查单ID，从数据库中加载所有信息
        :param check_id: 检查单ID
        :return:
        """
        # TODO:完成全部加载与按属性加载的功能

    def _write_info_to_database(self):
        """
        # TODO:信息写入数据库，可按属性写与全部写
        :return:
        """
        pass


class PatientMedicineInfo:
    """病人开药单中的信息类，每次医生的开药操作均生成一个该信息"""

    def __init__(self, diagnose_info: DiagnoseInfo, patient_medicine_id: int = None, medicine_info: List[tuple] = None):
        """初始化时必须传入诊断信息类"""
        self._patient_medicine_id = patient_medicine_id
        self._diagnose_info = diagnose_info
        self._medicine_info = medicine_info
        self._create_time = None

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
        self._medicine_info = medicine_info
        self._diagnose_info.add_medicine(medicine_id=self._patient_medicine_id)
        self._write_info_to_database(attr='all')

    def get_medicine_info(self):
        """
        获取开药信息
        :return:
        """
        return self._medicine_info

    def _write_info_to_database(self, attr):
        # TODO: 将当前信息写入数据库
        pass

    def _load_info_from_database(self):
        pass


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
        pass


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
            payment_info.create_id()
            diag_info.add_payment(payment_info.get_id())
        elif regs_id is not None:
            regs_info = RegisterInfo()
            regs_info.load_all_from_database(register_id=regs_id)
            payment_info = PaymentInfo(p_info, detail_info, diag_info=None, regs_info=regs_info)
            payment_info.create_id()
            regs_info.add_payment(payment_info.get_id())
        payment_info.cal_money()
        payment_info.create_payment()
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
        return p_info

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
        check_info.create_id()
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


class CommentSystem:
    """评论系统，用户对医生做出评价"""

    @staticmethod
    def make_comment(diagnose_id, comment_info):
        comment = CommentInfo(diagnose_id=diagnose_id)
        comment.make_comment(comment_info=comment_info)

    @staticmethod
    def find_all_comment(doctor_id):
        # TODO:提供医生id，返回所有评论，以列表形式返回
        return List


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
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)
        patient_check_info = PatientCheckInfo(diagnose_info=diag_info)

        patient_check_info.create_id()
        patient_check_info.create_prescribe_check(check_name=check_info)

        payment_info = PaymentSystem()
        payment_id = payment_info.create_payment_info(p_id=diag_info.get_patient_id(),
                                                      detail_info={i: 1 for i in check_info},
                                                      diag_id=diag_info.get_id())

        diag_info.add_payment(payment_id)

    @staticmethod
    def create_medicine(diagnose_id, medicine_info: List[tuple]):
        diag_info = DiagnoseInfo()
        diag_info.load_all_from_database(diagnose_id=diagnose_id)

        patient_medicine_info = PatientMedicineInfo(diagnose_info=diag_info)
        patient_medicine_info.create_id()
        patient_medicine_info.create_prescribe_medicine(medicine_info=medicine_info)

        payment_info = PaymentSystem()
        payment_id = payment_info.create_payment_info(p_id=diag_info.get_patient_id(),
                                                      detail_info=dict(medicine_info),
                                                      diag_id=diag_info.get_id())

        diag_info.add_payment(payment_id)

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


class CommentAnalysisSystem:
    """情感分析系统，主要分析病人评论，使用前需要初始化"""

    def __init__(self):
        self.stop_punctuation = string.punctuation + ':#0123456789，。！@#…*（）-+=】【】；：[]丶、~《》～？”' + ' ' + '\xa0' + '\n' + '\ue627' + '\r' + '\u3000'
        self.stop_list = []
        with open('LSTM_model/stopwords_list.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()  # 去除\n
                self.stop_list.append(line)
        with open('LSTM_model/dict_酒店.pkl', 'rb') as f:
            self.w2indx = pickle.load(f)  # 读取储存的数据
            self.w2vec = pickle.load(f)
        self.LSTM_model = load_model('LSTM_model/酒店_LSTM.h5')

    def single_predict(self, sentence):
        """
        输入一条单句，返回单句评分
        :param sentence: 单句
        :return: 评分，float
        """

        text = str(sentence)
        for punctuation in self.stop_punctuation:
            text = text.replace(punctuation, '')
        word_list = list(jieba.cut(text))

        for word in word_list:
            if word in self.stop_list:
                while word in word_list:
                    word_list.remove(word)

        new_sentences = []
        for word in sentence:
            new_sentences.append(np.array(self.w2indx.get(word, 0)))  # 单词转索引数字
        sentence_array = np.array([new_sentences])
        pad_sentence_array = sequence.pad_sequences(list(sentence_array), maxlen=150)
        predict_list = self.LSTM_model.predict(pad_sentence_array)
        print(sentence, predict_list[0][0])
        return predict_list[0][0]

    def multiple_predict(self, raw_sentence_list):
        """提供医生id，返回该医生的所有评价综合评分"""
        """很奇怪，输入数组的时候与输入单个句子会不一样，每生成一条评论就存一次数据库"""
        # raw_sentence_list = CommentSystem.find_all_comment(doctor_id)
        processed_text_list = []
        for text in raw_sentence_list:
            text = str(text)
            for punctuation in self.stop_punctuation:
                text = text.replace(punctuation, '')
            word_list = list(jieba.cut(text))
            for word in word_list:
                if word in self.stop_list:
                    while word in word_list:
                        word_list.remove(word)
            processed_text_list.append(word_list)

        new_sentences = []
        for sen in processed_text_list:
            new_sen = []
            for word in sen:
                new_sen.append(self.w2indx.get(word, 0))  # 单词转索引数字
            new_sentences.append(np.array(new_sen))
        sentence_array = np.array(new_sentences)  # 转numpy数组
        pad_sentence_array = sequence.pad_sequences(list(sentence_array), maxlen=150)
        predict_list = self.LSTM_model.predict(pad_sentence_array)
        predict_list = list(np.array(predict_list).reshape((len(predict_list),)))
        print(predict_list)
        return predict_list


class SearchSystem:
    """查询系统，可能用不上了"""
    pass


class AIDiagnoseSystem:
    """智能诊断系统"""
    pass


# TODO:有些类之间传类变量感觉冗余，能传id尽量传id。
# TODO:所有List[tuple]类型可直接改成dict，但会失去顺序，需讨论
# TODO:全部数据库连接工作未完成
# TODO:评论未完成
# TODO:某些状态检查支付没有做，要保证按顺序调用函数

CommentAnalysisSystem().single_predict('医术高明，妙手回春')
CommentAnalysisSystem().single_predict('垃圾医生')
CommentAnalysisSystem().multiple_predict(['医术高明，妙手回春', '垃圾医生'])
