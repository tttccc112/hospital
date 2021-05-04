import os
import sys
import time
import django
from typing import List, Dict, Tuple

BASE_DIR = os.path.dirname('/Users/xie/PycharmProjects/HospitalInformationSystem')
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HospitalInformationSystem.settings')
django.setup()


class NoAttrError(Exception):
    def __init__(self, target_attr, valid_attr, process):
        self.message = '流程{}错误!输入属性‘{}‘不在可行属性{}中'.format(process, target_attr, valid_attr)
        print(self.message)


class PatientInfo:
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
        更新患者在数据库/类中的信息
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
        if old_password != self._password:
            return False
        else:
            self._update_password(new_password)

    def get_info(self, attr: str):
        """
        获取患者的某项信息
        :param attr:需要获取的属性
        :return:
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
        self._id = p_id
        # 从数据库载入所有信息
        pass

    def write_all_to_database(self):
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

    def _load_all_from_database(self):
        pass

    def _load_info_from_database(self, attr: str):
        """
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
        将当前患者某个属性的信息写入数据库
        :param attr: 需要写入的属性
        :return:
        """
        pass


class RegisterInfo:
    def __init__(self):
        self._register_id = None
        pass

    def load_all_from_database(self, register_id):
        self._register_id = register_id
        pass

    def add_payment(self, payment_id):
        pass


class CheckInfo:
    check_money_dict = {}

    def __init__(self):
        pass


class MedicineInfo:
    medicine_money_dict = {}

    def __init__(self):
        pass


class PaymentInfo:
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
        return self._payment_id

    def get_status(self):
        return self._payment_status

    def create_payment(self):
        self._write_info_to_database()

    def update_status(self, new_status):
        if new_status not in [True, False]:
            raise NoAttrError(new_status, [True, False], '更新支付状态')
        else:
            self._payment_status = new_status
            if new_status:
                self._write_info_to_database()
            self._update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def load_all_from_database(self, payment_id):
        self._payment_id = payment_id
        # TODO:从数据库加载所有信息
        pass

    def cal_money(self):
        self._money = 0
        money_dict = dict(list(CheckInfo.check_money_dict.items()) + list(MedicineInfo.medicine_money_dict.items()))
        for detail in self._detail_info.items():
            if detail[0] not in money_dict.keys():
                raise NoAttrError(detail[0], money_dict.keys(), '计算缴费金额')
            else:
                self._money += money_dict[detail[0]] * detail[1]
        return self._money

    def _write_info_to_database(self):
        pass

    def create_id(self):
        # TODO:创建支付单ID
        self._update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 创建支付单时更新创建日期
        pass


class DiagnoseInfo:
    def __init__(self, patient_id: int = None, register_id: int = None, diagnose_id: int = None):
        self._patient_id = patient_id
        self._register_id = register_id
        self._diagnose_id = diagnose_id
        self._diagnose_info: str = ''
        self._diagnose_create_time = ''
        self._medicine_info = []
        self._check_info = []
        self._payment_info = []

    def add_diagnose(self, diagnose_info: str):
        self._diagnose_info += '\n------更新时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '------\n'
        self._diagnose_info += diagnose_info
        self._write_info_to_database('diagnose_info')

    def add_medicine(self, medicine_id):
        # 只存储开药单编号。
        self._medicine_info.append(medicine_id)
        self._write_info_to_database('medicine_info')

    def add_check(self, check_id):
        # 只存储检查单编号
        self._check_info.append(check_id)
        self._write_info_to_database('check_info')

    def add_payment(self, payment_id):
        self._payment_info.append(payment_id)
        self._write_info_to_database('payment_info')

    def get_id(self):
        return self._diagnose_id

    def create_id(self):
        self._diagnose_create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # TODO:创建ID函数
        pass

    def load_all_from_database(self, diagnose_id):
        self._diagnose_id = diagnose_id
        # TODO:提供ID，从database加载所有信息
        pass

    def _write_info_to_database(self, attr):
        pass


class PatientCheckInfo:
    # 病人检查单的信息，每次医生开检查就创建一个
    def __init__(self, diagnose_info: DiagnoseInfo, check_id: int = None):
        self._diagnose_info = diagnose_info  # 诊断类
        self._check_id = check_id  # 检查单ID
        self._check_name = []  # 检查名称列表，为需要做的检查
        self._check_info = {}  # 检查结果，为字典{检查名:结果}
        self._create_time = None
        self._last_update_time = None

    def create_prescribe_check(self, check_name: list = None):
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._check_name = check_name
        self._check_info = {i: None for i in check_name}
        self._write_info_to_database()
        self._diagnose_info.add_check(self._check_id)

    def create_id(self):
        return self._check_id

    def update_check_info(self, attr: str, value: float):
        if attr not in self._check_name:
            raise NoAttrError(attr, self._check_name, '更新检查信息')
        else:
            self._check_info[attr] = value
            self._last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self._write_info_to_database()
            # TODO:还需要更新病人身体详情

    def get_check_info(self, attr: str):
        if attr not in self._check_name:
            raise NoAttrError(attr, self._check_name, '更新检查信息')
        else:
            return self._check_info[attr]

    def _write_info_to_database(self):
        pass


class PatientMedicineInfo:
    # 病人开药单中的信息，每次医生的开药操作均生成一个该信息
    def __init__(self, diagnose_info: DiagnoseInfo, patient_medicine_id: int = None, medicine_info: List[dict] = None):
        self._patient_medicine_id = patient_medicine_id
        self._diagnose_info = diagnose_info
        self._medicine_info = medicine_info
        self._create_time = None

    def create_id(self):
        # TODO:增加创建id方法
        return self._patient_medicine_id

    def create_prescribe_medicine(self, medicine_info: List[dict]):
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._medicine_info = medicine_info
        self._diagnose_info.add_medicine(medicine_id=self._patient_medicine_id)
        self._write_info_to_database()

    def get_medicine_info(self):
        return self._medicine_info

    def _write_info_to_database(self):
        # TODO: 将当前信息写入数据库
        pass

    def _load_info_from_database(self):
        pass


class CommentInfo:
    def __init__(self, diagnose_id, comment_id=None):
        self._diagnose_id = diagnose_id
        self._comment_info = None
        self._create_time = None
        self._comment_trend = None
        self._comment_id = comment_id

    def create_id(self):
        # TODO: 创建id
        pass

    def make_comment(self, comment_info: str):
        self._comment_info = comment_info
        self._create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._cal_comment_trend()
        self._write_info_to_database()

    def _cal_comment_trend(self):
        # TODO:计算评价倾向评分
        pass

    def _write_info_to_database(self):
        # TODO: 将当前信息写入数据库
        pass


class PaymentSystem:
    def __init__(self):
        self._payment_info = None

    def create_payment_info(self, p_id: int, detail_info: dict, diag_id=None, regs_id=None):
        # TODO:改成传ID
        p_info = PatientInfo()
        p_info.load_all_from_database(p_id=p_id)
        if diag_id is not None and regs_id is not None:
            raise NoAttrError('同时输入注册单与挂号单', '仅可输入一种单据', '创建支付单')
        elif diag_id is not None:
            diag_info = DiagnoseInfo()
            diag_info.load_all_from_database(diagnose_id=diag_id)
            self._payment_info = PaymentInfo(p_info, detail_info, diag_info=diag_info, regs_info=None)
            self._payment_info.create_id()
            diag_info.add_payment(self._payment_info.get_id())
        elif regs_id is not None:
            regs_info = RegisterInfo()
            regs_info.load_all_from_database(register_id=regs_id)
            self._payment_info = PaymentInfo(p_info, detail_info, diag_info=None, regs_info=regs_info)
            self._payment_info.create_id()
            regs_info.add_payment(self._payment_info.get_id())
        return self._payment_info.get_id()

    def load_payment_info(self, payment_id):
        self._payment_info = PaymentInfo()
        self._payment_info.load_all_from_database(payment_id)

    def make_payment(self, payment_id):
        self.load_payment_info(payment_id)
        self._payment_info.update_status(True)
        return True


class PatientSystem:
    def __init__(self, patient_id):
        self._patient_id = patient_id

    def load_patient_info(self):
        p_info = PatientInfo(p_id=self._patient_id)
        p_info.load_all_from_database(p_id=self._patient_id)
        return p_info
        pass

    def registration(self, name, age, gender, password):
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
        self._patient_id = p_info.get_info('id')
        p_info.write_all_to_database()
        return p_info

    def update_info(self, attr, value):
        p_info = PatientInfo(p_id=self._patient_id)
        p_info.update_info(attr=attr, new_value=value)

    def update_password(self, old_password, new_password):
        p_info = PatientInfo(p_id=self._patient_id)
        p_info.update_password(old_password=old_password, new_password=new_password)


class MedicineSystem:
    def __init__(self, diagnose_id):
        self._diagnose_id = diagnose_id

    def add_medicine(self, medicine_id, add_num):
        # TODO:增加药品库存
        pass

    def prescribe_medicine(self, medicine_info_list: List[dict]):
        # 开药
        diagnose_info = DiagnoseInfo()
        diagnose_info.load_all_from_database(diagnose_id=self._diagnose_id)
        medicine_info = PatientMedicineInfo(diagnose_info=diagnose_info)
        medicine_info.create_id()
        medicine_info.create_prescribe_medicine(medicine_info_list)
        self._consume_medicine(medicine_info_list)

    def _consume_medicine(self, medicine_info_list):
        # TODO:减少数据库中的药品库存
        pass


class CheckSystem:
    def __init__(self, diagnose_id):
        self._diagnose_id = diagnose_id

    def prescribe_check(self, check_name_list: list):
        diagnose_info = DiagnoseInfo()
        diagnose_info.load_all_from_database(diagnose_id=self._diagnose_id)
        check_info = PatientCheckInfo(diagnose_info=diagnose_info)
        check_info.create_id()
        check_info.create_prescribe_check(check_name=check_name_list)

    def update_check_info(self):
        # TODO:级联更新检查信息
        pass


class CommentSystem:
    def __init__(self, diagnose_id):
        self._diagnose_id = diagnose_id

    def make_comment(self, comment_info):
        pass


class SearchSystem:
    pass

# TODO:有些类之间传类变量感觉冗余，能传id尽量传id。
