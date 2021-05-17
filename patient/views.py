from django.shortcuts import render

# Create your views here.

def test():
    print("hello world")

def home(request):
    return render(request,'home/homepage.html')
    
class Login():
    def __init__(self):
        pass
    
    def login(self,request):
        return render(request,'patient/login.html')