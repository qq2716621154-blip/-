import random

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from app01.models import UserInfo
def index(request):
    return HttpResponse('我是劳大')
def news(request):
    return render(request, 'news.html')
def xing(request):
    return render(request, 'xing.html')
def login(request):
    # 处理GET请求：显示登录页面
    if request.method == 'GET':
        return render(request, 'login.html')

    # 处理POST请求：验证表单数据
    elif request.method == 'POST':
        # 获取表单数据
        username = request.POST.get('text', '').strip()  # 对应表单中的name="username"
        password = request.POST.get('password', '').strip()  # 对应表单中的name="password"
        print(username, password)
        # 简单的表单验证
        errors = {}
        if not username:
            errors['username'] = '请输入用户名'
        if not password:
            errors['password'] = '请输入密码'

        # 如果有错误，返回登录页面并显示错误信息
        if errors:
            return render(request, 'login.html', {
                'login_errors': errors,
                'request': request  # 用于在模板中保留用户输入的值
            })

        # 这里添加实际的登录验证逻辑（例如与数据库中的用户信息比对）
        # 示例：假设用户名和密码都是'admin'则登录成功
        if username == 'admin' and password == 'admin':
            print('牛逼')
        else:
            # 登录失败，显示错误信息
            errors['non_field_errors'] = ['用户名或密码错误']
            return render(request, 'login.html', {
                'login_errors': errors,
                'request': request
            })

    # 处理其他请求方法
    else:
        return HttpResponse('不支持的请求方法', status=405)
def orm(request):
    UserInfo.objects.all().delete()
    UserInfo.objects.create(id='1',name='冉启康', password='woshisb', age=100),
    UserInfo.objects.create(id='2',name='李德烨', password='woshisb', age=100),
    UserInfo.objects.create(id='3',name='张婷', password='woshisb', age=100),
    UserInfo.objects.create(id='4',name='李晓洋', password='woshisb', age=100),
    return HttpResponse('操作成果')
def user_add(request):
    if request.method == 'POST':
        # 处理表单提交
        name = request.POST.get('name')
        password = request.POST.get('pwd')
        age = request.POST.get('age')
        print(name, password, age)
        UserInfo.objects.create(id=str(random.randint(0, 1000)), name=name, password=password, age=age)

        # 这里可以保存到数据库
        return redirect('user_list')  # 添加成功后跳转回用户列表
    if request.method == 'GET':
        return render(request, 'user_add.html')
def user_list(request):

    user_list = UserInfo.objects.all()
    print(user_list)
    return render(request, 'user_list.html',{'user_list': UserInfo.objects.all()})
def user_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    if request.method == 'GET':
        # 这里可以保存到数据库
        return redirect('user_list')  # 添加成功后跳转回用户列表