from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import SpiderDb
from django.shortcuts import redirect
from pyecharts.charts import Bar,Pie
from pyecharts import options as opts
# Create your views here.
def show_data(request):
    objs = SpiderDb.objects.all()
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
    else:
        bar = Bar()
        bar.add_xaxis([obj.author for obj in objs])
        bar.add_yaxis("正面", [round(obj.positive,2) for obj in objs])
        bar.add_yaxis("中性", [round(obj.neutral,2) for obj in objs])
        bar.add_yaxis("负面", [round(obj.negative,2) for obj in objs])
        bar.set_global_opts(title_opts=opts.TitleOpts(title="舆情分析")
                            ,yaxis_opts=opts.AxisOpts(name="情感趋势")
                            ,xaxis_opts=opts.AxisOpts(name="媒体"))
        chart = bar.render_embed()
        return render(request,'analysis.html',{"objs":objs,"chart":chart})

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

def author(request,topic,author):
    objs = SpiderDb.objects.filter(topic=topic,author=author).all()
    if not objs:
        return redirect("/")
    else:
        pie = Pie()
        charts = []
        for obj in objs:
            pie.add("",[("积极",obj.positive),("中立",obj.neutral),("消极",obj.negative)],radius=[80,150])
            pie.set_global_opts(title_opts=opts.TitleOpts(title=obj.author,
                                                          pos_left="center",
                                                          pos_bottom="center"),
                                legend_opts=opts.LegendOpts(pos_left="left",
                                                            orient="vertical"))
            charts.append(pie.render_embed())
        return render(request,'author.html',{"objs":objs,"charts":charts})
