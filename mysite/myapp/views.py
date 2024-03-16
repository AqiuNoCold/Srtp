from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import SpiderDb
# Create your views here.
def user_list(request):
    Topic = SpiderDb.objects.all()
    for obj in Topic:
        print(obj.origin,obj.author)
    print(request.method)
    print(request.GET)
    name = "Wan"
    roles = ["Admin","User","Guest"]
    user_info = {"name":"YiHan","age":24,"gender":"Male"}
    # 可以直接选择抓包获取数据！！！
    # import requests
    # r = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    #return redirect("https://www.baidu.com")
    return render(request,'user_list.html',{"n1":name,"n2":roles,"n3":user_info})

def login(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("username") == "admin" and request.POST.get("password") == "123456":
            return HttpResponse("登陆成功")
        else:
            return render(request,'login.html',{"error_msg":"用户名或密码错误"})
    if request.method == "GET":
       return render(request,'login.html')