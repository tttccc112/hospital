import numpy as np
import pandas as pd
import pickle
from xgboost import XGBClassifier
from doctor.models import *
from patient.models import *
from django.forms.models import model_to_dict     # 将models转化为dict


class Decide:
    def __init__(self):
        pass

    @classmethod
    def get_decide_attr(cls,pid):
        """
        根据病人号pid加载当前病人所有检查结果
        :param pid: 病人号
        :return: 字典，{各属性}   （由于属性太多，请给每个属性都取个名字，然后把值传给我，没有就空字符串）
        """
        attr_dict = PatientHealth.objects.filter(pid_id=pid) # 最新的
        attr_dict = model_to_dict(attr_dict[len(attr_dict)-1])   # 最新的,属性字典
        for key,value in attr_dict.items():
            if value == None:
                attr_dict[key] = ""
        print(attr_dict)
        return attr_dict


    @classmethod
    def predict(cls,pid):
        """
        根据病人最后一次住院的检查记录判别疾病类型
        :param pid: 病人号
        :return: 判别结果(1代表陈旧性心梗,2代表急性心梗)
        """
        test_dict = PatientHealth.objects.filter(pid_id=pid).select_related()
        test = pd.DataFrame(list(test_dict.values())).iloc[-1]
        test = test.drop(['pdate','id','pid_id'])  # 提取属性

        loaded_model = pickle.load(open("classifier.pkl", "rb"))
        # print(test)
        y_pred = loaded_model.predict(np.array(test).reshape((1,-1)))  # 只预测一个样本,需要转换维度
        print(y_pred)   # 显示预测结果
        return  y_pred


    # @classmethod
    # def predict(cls,pid):  error
    #     """
    #     对患者的情况进行预测
    #     :param pid:
    #     :return:
    #     """
    #     # 准备数据
    #     test_dict = PatientHealth.objects.filter(pid_id=pid).select_related()
    #     test = pd.DataFrame(list(test_dict.values())).iloc[-1]
    #     # print(test_X)
    #     test_id = test["id"]
    #     train_dict = PatientHealth.objects.exclude(id=test_id)
    #     train = pd.DataFrame(list(train_dict.values()))
    #     # print(train_X.head())
    #
    #     # 构建分类器
    #     clf = XGBClassifier()

