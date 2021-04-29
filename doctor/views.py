from django.shortcuts import render
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.shortcuts import render,HttpResponse

from doctor import models
from doctor.models import Remark,Department,Medicine,\
    CheckItem,DoctorBase,Check,CheckDetail,Roster



import xlrd


# Create your views here.
def test():
    print("hello world")


# def load(file):
#     data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\"+file)
#     table = data.sheets()[0]
#     nrows = table.nrows
#     return table,nrows


def load3(request):
    """
    D3 部门表
    """
    DepartmentList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D3科室表.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            # D6
            temp = table.row_values(i)
            dept_id,dept_name,doc_id= temp[0],temp[2],temp[1]
            # doc_id_instance = DoctorBase.filter(doc_id=doc_id)
            DepartmentList.append(models.Department(dept_id=dept_id,dept_name=dept_name,
                                                    doc_id_id = doc_id))
    Department.objects.bulk_create(DepartmentList)
    return HttpResponse("D3完成!")

def load4(request):
    """
    D4 药品价格信息
    """
    MedicineList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D4药品价格信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            # D6
            temp = table.row_values(i)
            med_id,med_name,med_class,med_price,med_stock,initial_py = temp[0],\
                                      temp[1],temp[2],temp[3],temp[4],temp[5]
            # doc_id_instance = DoctorBase.filter(doc_id=doc_id)
            MedicineList.append(models.Medicine(med_id = med_id,med_name=med_name,med_class=med_class,
                                                  med_price=med_price,med_stock = med_stock,initial_py=initial_py))
    Medicine.objects.bulk_create(MedicineList)
    return HttpResponse("D4完成!")

def load5(request):
    """
    D5 检查价格信息
    """
    CheckItemList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D5检查价格信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            # D6
            temp = table.row_values(i)
            check_id,check_name,check_price = temp[0],temp[1],temp[2]
            CheckItemList.append(models.CheckItem(check_id=check_id,check_name=check_name,check_price=check_price))
    CheckItem.objects.bulk_create(CheckItemList)
    return HttpResponse("D5完成!")

def home(request):
    # D6 医生基本信息
    DoctorBaseList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D6医生信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            # D6
            temp = table.row_values(i)
            docid,deptid,title,docname,password = temp[0],temp[1],temp[2],temp[3],temp[4]
            DoctorBaseList.append(models.DoctorBase(doc_id=docid,dept_id=deptid,doc_title=title,doc_name=docname,password=password))
    DoctorBase.objects.bulk_create(DoctorBaseList)
    return HttpResponse("D6完成!")

def load9(request):
    """
    D9 检查信息
    """
    CheckList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D9检查信息.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            temp = table.row_values(i)
            report_id,diagnose_id,pid,check_list,chest =  temp[0],temp[1],temp[2],temp[3],temp[4]
            CheckList.append(models.Check(report_id=report_id,diagnose_id_id=diagnose_id,
                                          pid_id=pid,check_list=check_list,chest=chest))
    Check.objects.bulk_create(CheckList)
    return HttpResponse("D9完成!")
    # 需要先写D11病人表和D8诊断表

def load12(request):
    pass

def load14(request):
    pass




