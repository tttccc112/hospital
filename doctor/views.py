import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import xlrd
import pandas as pd
import json
import datetime

from django.shortcuts import render,HttpResponse
from doctor.models import Remark,Department,Medicine,\
    CheckItem,DoctorBase,Check,CheckDetail,Roster

from doctor import dmethod
from doctor import models

from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def test():
    print("hello world")


class index(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #index页面独有（根据医生doc和患者pat获得的“最新”“挂号ID”下的信息：
        #1、基本信息：字典形式{姓名，性别，生日，挂号ID}
        #2、已开检查：字典列表，【{ID，名称，时间，状态（三种：未缴费、已缴费、已结束）}，{}，{}】
        #3、可以开具的检查（静态固定的6种检查）：字典列表：【{ID，名称}，{}】
        #4、诊断内容：文本
        #5、已开药品：字典列表，【{ID，名称，数量}，{}，{}】

        return render(request,'index.html')


    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='check':
            check_ids=request.POST.getlist('check_ids')
            #将要开的检查存入数据库，得到一个ID列表，写入当前诊断ID或者挂号ID下的数据库中
            return HttpResponse(json.dumps(ret))
        elif entrance=='save_medicine':
            medi_num=request.POST.getlist('medi_num')
            #将要开的药品存入数据库：【（ID，数量），】，如果数量检测为0，在原数据库中删除该药品
            return HttpResponse(json.dumps(ret))
        elif entrance=='search_medicine':
            abbreviated=request.POST.get('abbreviated')
            #根据所得简写检索得到药品列表[id，名称]，改写message后发送给前端
            ret['message']=[['0','好吃药'],['1','难吃药']]
            return HttpResponse(json.dumps(ret))
        elif entrance=='save_discription':
            #更新诊断数据库
            text=request.POST.get('text')
            return HttpResponse(json.dumps(ret))
        elif entrance=='search_check':
            #提供该检查id下的详情，根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))


class history(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #history网页独有，当前患者ID下的所有历史诊断ID：
        #1、字典列表：【{诊断ID，科室，诊断}，{}，{}】
        return render(request,'history.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='his':
            #根据诊断ID获取详细信息：
            #1、基本信息：字典形式{姓名，性别，生日，挂号ID}
            #2、已开检查：字典列表，【{ID，名称，时间，状态（三种：未缴费、已缴费、已结束）}，{}，{}】
            #3、诊断内容：文本
            #4、已开药品：字典列表，【{ID，名称，数量}，{}，{}】

            return HttpResponse(json.dumps(ret))
        elif entrance=='search_check':
            #提供该检查id下的详情
            #根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))

class check(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #check网页独有，当前患者ID下的所有历史检查ID：
        #1、字典列表：【{检查ID，日期，名称，诊断}，{}，{}】
        return render(request,'check.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='ch':
            return HttpResponse(json.dumps(ret))
        elif entrance=='search_check':
            #提供该检查id下的详情
            #根据检查ID得到【名称，时间，【属性列表】，【对应值列表】】
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))


class decide(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #decide网页独有：
        #1、字典，{各属性}   （由于属性太多，请给每个属性都取个名字，然后把值传给我，没有就空字符串）
        dmethod.Decide.get_decide_attr("19794")  # 返回字典，{各属性}
        a = dmethod.Decide.predict("19794")
        print(a)
        return render(request,'decide.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}

        dmethod.Decide.predict("19794")  # 返回1或者2,分别表示陈旧性和急性心梗

        if entrance=='result':
            #返回诊断结果
            #直接根据数据库中的数据判别后传给我
            ret['message']='急性心梗'
            return HttpResponse(json.dumps(ret))


class arrange(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #arrange网页独有,当前医生doc下的本日病人：
        #1、字典列表，【{病人ID，姓名，年龄}，{}，{}】
        #2、列表，周一到周五的安排看诊数【1,2,3,4,5,6,7】
        return render(request,'arrange.html')

    def post(self,request,doc,pat):
        pass


class evaluation(View):
    def get(self,request,doc,pat):
        #所有网页共用：
        #1、 某医生ID下的已看病人数和未看病人数，【已看病人数，未看病人数】
        #2、某医生ID下的已看病人，字典形式：{ID，姓名，年龄}
        #3、当前医生ID下的评级和好评比率，【星级数，好评比率】
        #evaluation网页独有,当前医生doc下评价：
        #1、不同星级的评价数，列表【一星，二星，三星，四星，五星】
        #2、好评数、差评数，【好评数，差评数】
        #近期评价，【{1，日期，内容，星级}，{2，日期，内容，星级}，{3，日期，内容，星级}】按时间排序并根据顺序给出ID
        return render(request,'evaluation.html')

    def post(self,request,doc,pat):
        pass

def profile(request,doc,pat):
    return render(request,'profile.html')



"""导入数据库"""
# Create your views here.
def test():
    print("hello world")


def load2(request):
    """
    D2 医生评价信息
    """
    RemarkList = []
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D2医生评价信息.xls")
    # nrows = data.shape[0]  # 获取表的行数
    for ind,row in data.iterrows():
        remark_id,diagnose_id,doc_id,remark_date,remark,score =row[0],\
            row[1],row[2],row[3],row[4],row[5]  # date in excel -> string in python
        RemarkList.append(models.Remark(remark_id=remark_id, remark_date=remark_date,
                                        remark=remark, diagnose_id_id=diagnose_id,
                                        score=score, doctor_id_id=doc_id))
    Remark.objects.bulk_create(RemarkList)
    return HttpResponse("D2完成!")



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
            DoctorBaseList.append(models.DoctorBase(doc_id=docid,dept_id=deptid,doc_title=title,
                                                    doc_name=docname,password=password))
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
    CheckDetailList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D12检查详情.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            temp = table.row_values(i)
            diagnose_id,detail_id,check_id,result,time,status = temp[0], temp[1], temp[2], temp[3], temp[4],temp[5]
            CheckDetailList.append(models.CheckDetail(diagnose_id_id=diagnose_id,detail_id=detail_id,
                                            check_id_id=check_id,report_content=result,check_time=time,check_status=status))
    CheckDetail.objects.bulk_create(CheckDetailList)
    return HttpResponse("D12完成!")

def load14(request):
    RosterList = []
    data = xlrd.open_workbook("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D14排版表.xls")
    table = data.sheets()[0]
    nrows = table.nrows  # 获取表的行数
    for i in range(nrows):
        if i == 0:
            continue
        else:
            temp = table.row_values(i)
            doc_id,reamin,regis_list = temp[0], temp[1], temp[2]
            RosterList.append(models.Roster(doc_id_id=doc_id,remain=reamin,reservations=regis_list))
    Roster.objects.bulk_create(RosterList)
    return HttpResponse("D14完成!")


def encrypt(request):
    """
    D6 转换成加密存储
    """
    data = pd.read_excel("E:\\大三下2021春\\01信息系统分析与设计\\project\\data\\D6医生信息_new.xls")
    #password = data['password']
    #encrypted_password = data['encrypted_password']
    for ind,row in data.iterrows():
        password = row['password']
        encrypted_password = row['encrypted_password']
        # print(password,encrypted_password)
        a = DoctorBase.objects.filter(password=password).update(password=encrypted_password)
        # a.password = encrypted_password
        # print(a)
    return HttpResponse('D6加密完成')


