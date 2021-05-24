from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
import datetime
import time
# Create your views here.


# 首页类
def home(request):
    return render(request, 'home/homepage.html')


# 登录页面类
class Loginclass(View):

    def get(self, request):
        return render(request, 'patient/login.html')

    def post(self, request):

        patient_id = request.POST.get('patient_id', None)
        patient_pwd = request.POST.get('patient_pwd', None)

        # 这里改成从数据库中获取账号与密码哈希
        if patient_id == 'root' and patient_pwd == '123123':
            return redirect("/patient/index/"+str(patient_id)+'/')
        else:
            # 返回用户界面
            return render(request, 'patient/login.html', {'warn': '密码或ID错误'})

            

# 用户注册
class Signupclass(View):
    def get(self,request):
        return render(request, 'patient/signup.html')
    
    def post(self,request):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/base.html')
        else:
            return render(request, 'patient/signup.html', {'warn': '两次密码不一致'})
        




# remained
class Index(View):
    def get(self,request,pat):
        return render(request, 'patient/index.html')
    
    def post(self,request,pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/base.html')
        else:
            return render(request, 'patient/signup.html', {'warn': '两次密码不一致'})
        
        
# remained
class Case_history(View):
    def get(self,request,pat):
        return render(request, 'patient/case_history.html')
    
    def post(self,request,pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')
        
# remained
class Check(View):
    def get(self,request,pat):
        return render(request, 'patient/check.html')
    
    def post(self,request,pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')

# remained
class Fee(View):
    def get(self,request,pat):
        return render(request, 'patient/fee.html')
    def post(self,request,pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')
    

# 尚未完成
class Feedback(View):
    def get(self,request,pat):
        return render(request, 'patient/feedback.html')
    def post(self,request,pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')
        
        
    
        
# 在完成中 挂号系统1
class Register(View):
    def get(self,request,pat):
        print(request.user)
        print(request.path)
        
        return render(request, 'patient/register.html')
    
    def post(self,request,pat):
        print(request.user)
        print(request.path)
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')


# 挂号系统2
class Register2(View):
    def get(self,request,pat,out_pat):
        print(out_pat)
        # 接口处
        # 输入一个科室 返回本日及七天后的该科室医生排班信息
        datetime.datetime.now().strftime('%m-%d-%w')
        return render(request, 'patient/register2.html',{'out_pat':out_pat})
    
    def post(self,request,pat):
        print(request.user)
        print(request.path)
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd==repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')
    