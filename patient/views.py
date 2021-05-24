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
    D7 费用表
    """
    FeeList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D7流水单.xls")
    # Cannot assign ... must be a ... instance  可能是漏了_id_id
    for ind,row in data.iterrows():
        fee_id,register_id_id,diagnose_id_id,fee_content,fee_total,fee_date \
                = row[0],row[1],row[2],row[3],row[4],row[5]
        print(fee_id,register_id_id,diagnose_id_id,fee_content,fee_total,fee_date)

        if register_id_id != register_id_id: register_id_id = None
        if diagnose_id_id != diagnose_id_id: diagnose_id_id = None

        FeeList.append(models.Fee(fee_id=fee_id,register_id_id=register_id_id,
                                  diagnose_id_id=diagnose_id_id,fee_content=fee_content,
                                  fee_total=fee_total,fee_date=fee_date))
        # FeeList.append(models.Fee(fee_id=fee_id,diagnose_id_id=diagnose_id_id,fee_content=fee_content,
        #                           fee_total=fee_total, fee_date=fee_date))
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

def setnone(x):
    if x!=x:
        return None
    else:
        return x

def load13(request):
    """
    D13 患者身体信息
    """
    PatientHealthList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D13患者身体信息.xls")
    # Cannot assign ... must be a ... instance  可能是漏了_id_id
    for ind,row in data.iterrows():
        pid,pdate,pgender,page,low_bp,high_bp,ast,alat,tp,alb,glb,ag,tg,tc,\
        glc,hdl,ldl,cre,tt,fg,aptt,pt,ck,ckmb,cTnI,ct,stt,stup,std,q = \
        row[0],row[1],row[2],row[3],setnone(row[4]),setnone(row[5]),setnone(row[6]),setnone(row[7]),setnone(row[8]),setnone(row[9]),setnone(row[10]),\
        setnone(row[11]),setnone(row[12]),setnone(row[13]),setnone(row[14]),setnone(row[15]),setnone(row[16]),setnone(row[17]),setnone(row[18]),setnone(row[19]),setnone(row[20]),\
        setnone(row[21]),setnone(row[22]),setnone(row[23]),setnone(row[24]),row[25],row[26],row[27],row[28],row[29]
        # print(pid,pdate,pgender,page,low_bp,high_bp,ast,alat,tp,alb,glb,ag,tg,tc,\
        #     glc,hdl,ldl,cre,tt,fg,aptt,pt,ck,ckmb,cTnI,ct,stt,stup,std,q)
        PatientHealthList.append(models.PatientHealth(pid_id=pid,pdate=pdate,pgender=pgender,page=page,low_bp=low_bp,high_bp=high_bp,
                                                      ast=ast,alat=alat,tp=tp,alb=alb,glb=glb,ag=ag,tg=tg,tc=tc,glc=glc,hdl=hdl,ldl=ldl,
                                                      cre=cre,tt=tt,fg=fg,aptt=aptt,pt=pt,ck=ck,ckmb=ckmb,cTnI=cTnI,ct=ct,stt=stt,
                                                      stup=stup,std=std,q=q))
    PatientHealth.objects.bulk_create(PatientHealthList)
    return HttpResponse("D13完成!")
