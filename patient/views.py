from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
# Create your views here.


def test():
    print("hello world")

# 首页类
def home(request,doc,pat):
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
            return redirect("/patient/base")
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
        



def base(request):
    return render(request, 'patient/base.html')


# 用户界面
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
        
        

# 病例
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