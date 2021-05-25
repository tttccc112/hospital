from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.template import RequestContext
import datetime
import time
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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
    def get(self, request):
        return render(request, 'patient/signup.html')

    def post(self, request):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/base.html')
        else:
            return render(request, 'patient/signup.html', {'warn': '两次密码不一致'})


# remained
class Index(View):
    def get(self, request, pat):
        return render(request, 'patient/index.html')

    def post(self, request, pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/base.html')
        else:
            return render(request, 'patient/signup.html', {'warn': '两次密码不一致'})


# remained
class Case_history(View):
    def get(self, request, pat):
        return render(request, 'patient/case_history.html')

    def post(self, request, pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')

# remained


class Check(View):
    def get(self, request, pat):
        return render(request, 'patient/check.html')

    def post(self, request, pat):
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')

# 缴费页面 未完成，需要设计缴费按钮  05-25-11:22
# remained
class Fee(View):
    def get(self, request, pat):
        # 接口
        # 输入患者id，返回患者缴费信息
        return render(request, 'patient/fee.html')

    def post(self, request, pat):
        # 接口
        # 输入检查id，患者id，日期，生成缴费信息（缴费id等）

        return render(request, 'patient/fee.html', context_instance =RequestContext(request))


# 反馈页面, 基本完成 05-25-11:16
class Feedback(View):
    def get(self, request, pat):
        return render(request, 'patient/feedback.html')

    def post(self, request, pat):
        # 获取用户的反馈信息
        feedback_msg = request.POST.get('feedback_msg', None)
        if feedback_msg=='':
            return render(request, 'patient/feedback.html')
        
        else:
            print(feedback_msg)
            # 接口
            # 将反馈信息写入数据库
            return render(request, 'patient/feedback.html', {'bfr': feedback_msg+'成功提交'})


# 基本完成 挂号系统1（选择挂号科室） 05-23
class Register(View):
    def get(self, request, pat):
        print(request.user)
        print(request.path)

        return render(request, 'patient/register.html')


# 挂号系统2 未完全完成，需要根据返回信息设计动态显示 05-24
class Register2(View):
    def get(self, request, pat, out_pat):
        #out_pat为门诊科室名 如小儿内科门诊
        # 接口处
        # 输入一个科室 返回本日及七天后的该科室医生排班信息
        datetime.datetime.now().strftime('%m-%d-%w')
        return render(request, 'patient/register2.html', {'out_pat': out_pat})

    def post(self, request, pat):
        print(request.user)
        print(request.path)
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')

# 挂号系统3 未完全完成 需要根据返回信息动态显示并且设计缴费机制 05-24
class Register3(View):
    def get(self, request, pat, department, doc):
        # 接口处
        # 输入医生id得到医生姓名，科室，职称的字典
        dic = {'doc_docname': '谢谢谢', 'doc_title': '副主任医师', 'doc_dep': '德国骨科'}
        return render(request, 'patient/register3.html', dic)

    def post(self, request, pat, department, doc):
        print(request.user)
        print(request.path)
        pid = request.POST.get('patient_id', None)
        pname = request.POST.get('patient_name', None)
        pbirth = request.POST.get('patient_birthday', None)

        repeat_pwd = request.POST.get('repeat_pwd', None)
        patient_pwd = request.POST.get('patient_pwd', None)
        if patient_pwd == repeat_pwd:
            return render(request, 'patient/case_history.html')
        else:
            return render(request, 'patient/case_history.html')
