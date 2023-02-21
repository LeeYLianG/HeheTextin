from django import forms
from django.shortcuts import render, redirect
from hehe import models
from requests import request

from ..utils.encrypt import md5


class LoginForm(forms.Form):
    username=forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    passwrod=forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    def clean_passwrod(self):
        password=self.cleaned_data.get('password')
        return md5(password)

def login(request):
    title='登录页面'
    if request.method=='GET':
        form=LoginForm()
        return render(request,'change.html',{'form':form,'title':title})
    if request.method =='POST':
        form=LoginForm(data=request.POST)
        if form.is_valid():
            admin_object=models.Admin.objects.filter(**form.cleaned_data).first()
            if not admin_object:
                form.add_error('passwrod','用户名或密码错误')
                return render(request,'login.html',{'form':form,'title':title})
            request.session['info']={"id":admin_object.id,'username':admin_object.username}
            return redirect('admin/list/')
    return render(request, 'login.html', {'form': form,'title':title})



def logout(request):
    request.session.clear()

    return redirect('login/')