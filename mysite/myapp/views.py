from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import SpiderDb
from django.shortcuts import redirect
from pyecharts.charts import Bar
# Create your views here.
def show_data(request):
    objs = SpiderDb.objects.all()
    # name = "Wan"
    # roles = ["Admin","User","Guest"]
    # user_info = {"name":"YiHan","age":24,"gender":"Male"}
    # 可以直接选择抓包获取数据！！！
    # import requests
    # r = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    # return redirect("https://www.baidu.com")
    return render(request,'show_data.html',{"objs":objs})

def login(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("username") == "admin" and request.POST.get("password") == "123456":
            return redirect("/show/data")
        else:
            return render(request,'login.html',{"error_msg":"用户名或密码错误"})
    if request.method == "GET":
        return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def analysis(request,topic):
    objs = SpiderDb.objects.filter(topic=topic).all()
    if not objs:
        return (redirect("/"))
    return render(request,'analysis.html',{"objs":objs})

def delete(request,id):
    SpiderDb.objects.filter(id=id).delete()
    return redirect("/show/data")

def search(request):
    if request.method == "POST":
        text = request.POST.get("text")
        objs = SpiderDb.objects.filter(topic=text).all()
        if not objs:
            return render(request,'search.html',{"error_msg":"没有找到相关数据"})
        else:
            return render(request,'search.html',{"objs":objs})

