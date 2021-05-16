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

        return render(request,'index.html')


    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='check':
            check_ids=request.POST.getlist('check_ids')
            #将要开的检查存入数据库
            return HttpResponse(json.dumps(ret))
        elif entrance=='save_medicine':
            medi_num=request.POST.getlist('medi_num')
            #将要开的药品存入数据库
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
            #提供该检查id下的详情
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))


class history(View):
    def get(self,request,doc,pat):

        return render(request,'history.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='his':
            return HttpResponse(json.dumps(ret))
        elif entrance=='search_check':
            #提供该检查id下的详情
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))

class check(View):
    def get(self,request,doc,pat):

        return render(request,'check.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='ch':
            return HttpResponse(json.dumps(ret))
        elif entrance=='search_check':
            #提供该检查id下的详情
            id=request.POST.get('id')
            ret['message']=['尿检','2000-1-12',['DNA','RNA'],['1','0.9']]
            return HttpResponse(json.dumps(ret))


class decide(View):
    def get(self,request,doc,pat):

        return render(request,'decide.html')

    def post(self,request,doc,pat):
        entrance=request.POST.get('entrance')
        ret={'status':True,'message':None}
        if entrance=='result':
            #返回诊断结果
            ret['message']='急性心梗'
            return HttpResponse(json.dumps(ret))


def arrange(request,doc,pat):
    return render(request,'arrange.html')

def evaluation(request,doc,pat):
    return render(request,'evaluation.html')