from django.forms import models
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from ..models import User
from django import forms
from django.core.exceptions import ValidationError


# Create your views here.
# ModelForm
class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
#钩子方法：校验用户提交的数据
    def clean_phone(self):
        post_phone = self.cleaned_data['phone']
        if post_phone != 11 or post_phone[0] != 1:
            raise ValidationError('手机号码格式错误')


# 注册
def registerView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if User.objects.filter(username=username,password=password1).exists():
            msg = '用户已存在'
        elif password1 != password2:
            msg = '密码输入不一致'
        else:
            user = User.objects.create(username=username, password=password1, email=email, phone=phone)
            msg = '注册成功'
            return redirect("users/login/")
    return render(request, "users_register.html", locals())


# 登录
def loginView(request):
    if request.method == 'GET':
        return render(request, 'users_login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                msg = '登录成功'
            else:
                msg = '用户名或密码错误'
        else:
            msg = '用户不存在,请先注册'
    return render(request, "users_login.html", locals())


# 编辑用户信息
def user_edit(request, nid):
    title='用户编辑页面'
    nid_object = User.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据id获取要编辑的对象
        form = UserModelForm(instance=nid_object)
        return JsonResponse(form)
    else:
        form = UserModelForm(data=request.POST, instance=nid_object)
        if form.is_valid():
            form.save()
            return redirect('users/main/')
    return render(request, 'change.html', {'from': form, 'title': title})

