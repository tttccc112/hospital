from django.shortcuts import render
from django.shortcuts import render
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.shortcuts import render,HttpResponse

from patient import models
from patient.models import Register,Fee,Diagnose,\
    Prescribe,PatientBase,PatientHealth

import xlrd
import pandas as pd
import datetime
# Create your views here.

def test():
    print("hello world")

def test2():
    print("hello world!")
    
def test5():
    print('?')

def load1_(request):
    """
    D3 挂号表
    """
    RegisterList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D1挂号信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            temp = table.row_values(i)
            register_id,pid_id,doc_id,dept_id,register_date,status = temp[0], \
                    temp[1],temp[2],temp[3],temp[4],temp[5]  # date in excel -> string in python
            register_date = datetime.datetime(register_date)  #.strftime('%Y-%m-%d')
            print(register_date)
            RegisterList.append(models.Register(register_id=register_id,pid_id=pid_id,doc_id_id=doc_id,
                                                dept_id_id=dept_id,register_date=register_date,status=status))
    Register.objects.bulk_create(RegisterList)
    return HttpResponse("D1完成!")

def load1(request):
    """
    D1 挂号表
    """
    RegisterList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D1挂号信息.xls")
    # nrows = data.shape[0]  # 获取表的行数
    for ind,row in data.iterrows():
        register_id, pid_id, doc_id, dept_id, register_date, status = row[0], \
                            row[1], row[2], row[3], row[4], row[5]  # date in excel -> string in python
        # register_date = datetime.datetime(register_date)  # .strftime('%Y-%m-%d')
        RegisterList.append(models.Register(register_id=register_id, pid_id=pid_id, doc_id_id=doc_id,
                                            dept_id_id=dept_id, register_date=register_date, status=status))
    Register.objects.bulk_create(RegisterList)
    return HttpResponse("D1完成!")

def load8(request):
    """
    D8 诊断表
    """
    DiagnoseList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D8诊断记录.xls")
    for ind,row in data.iterrows():
        diagnose_id,register_id,pid,diagnose_text,diagnose_date,medicine_id,report_id,fee_id \
            = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]
        DiagnoseList.append(models.Diagnose(diagnose_id=diagnose_id,register_id_id=register_id,
                                            pid_id=pid,diagnose_text=diagnose_text,
                                            diagnose_date=diagnose_date,medicine_id=medicine_id,
                                            report_id=report_id,fee_id=fee_id))
    Diagnose.objects.bulk_create(DiagnoseList)
    return HttpResponse("D8完成!")

def load7(request):
    """
    D10 开药记录表
    """
    FeeList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D7流水单.xls")
    # Cannot assign ... must be a ... instance  可能是漏了_id_id
    for ind,row in data.iterrows():
        fee_id,register_id_id,diagnose_id_id,fee_content,fee_total,fee_date \
                = row[0],row[1],row[2],row[3],row[4],row[5]
        FeeList.append(models.Fee(fee_id=fee_id,register_id_id=register_id_id,
                                  diagnose_id_id=diagnose_id_id,fee_content=fee_content,
                                  fee_total=fee_total,fee_date=fee_date))
    Fee.objects.bulk_create(FeeList)
    return HttpResponse("D7完成!")

def load10(request):
    """
    D10 开药记录表
    """
    PrescribeList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D10开药记录.xls")
    # Cannot assign ... must be a ... instance  可能是漏了_id_id
    for ind,row in data.iterrows():
        prescribe_id,diagnose_id,prescribe_content= row[0],row[1], row[2]
        PrescribeList.append(models.Prescribe(prescribe_id=prescribe_id,diagnose_id_id=diagnose_id,prescribe_content=prescribe_content))
    Prescribe.objects.bulk_create(PrescribeList)
    return HttpResponse("D10完成!")

def load11(request):
    """
    D11 病人信息表
    """
    PatientBaseList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D11患者信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            temp = table.row_values(i)
            pid,pname,pgender,pbirth,password = temp[0],temp[1],temp[2],temp[3],temp[4]  # date in execl -> string in python
            PatientBaseList.append(models.PatientBase(pid=pid,pname=pname,pgender=pgender,pbirth=pbirth,password=password))
    PatientBase.objects.bulk_create(PatientBaseList)
    return HttpResponse("D11完成!")
