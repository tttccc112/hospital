from django.shortcuts import render,HttpResponse
from doctor import models
import json
import time
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
        return render(request,'decide.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
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