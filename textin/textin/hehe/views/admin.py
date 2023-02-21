import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..models import Admin
from django.http import JsonResponse
from django.core import serializers
from hehe import models
from ..utils.encrypt import md5
from django import forms
from django.core.exceptions import ValidationError

class AdminModelForm(forms.ModelForm):
    again_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'again_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_again_password(self):
        password = self.cleaned_data.get('password')
        again_password = self.cleaned_data.get('again_password')
        if again_password != password:  # 判断两次密码是否相同
            raise ValidationError('密码不一致')
        elif password:  # 判断密码不为空或一致的情况
            return md5(password)
        else:
            raise ValidationError('密码不能为空')

class AdminResetModelForm(forms.ModelForm):
    again_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields = ['password','again_password']
    def clean_again_password(self):
        password = self.cleaned_data.get('password')
        again_password = self.cleaned_data.get('again_password')
        if again_password != password:  # 判断两次密码是否相同
            raise ValidationError('密码不一致')
        elif password:  # 判断密码不为空或一致的情况
            return md5(password)
        else:
            raise ValidationError('密码不能为空')


def adminView(request):
    title='管理员列表'
    if request.method=='GET':
        data_dict = {}
        search_data = request.GET.get('username', '')
        if search_data:
            data_dict['username__contains'] = search_data
            queryset = models.Admin.objects.filter(**data_dict).order_by('id')
            json_data = serializers.serialize('json', queryset)
            json_data = json.loads(json_data)
            json_dict = {
                    'search_data':search_data,
                    'json_data':json_data,
                    'title':title
                }
        return JsonResponse(json_dict)

        # else:
        #     queryset = models.Admin.onjects.all()
        #     json_dict={
        #         'url':'admin/list/',#需跳转的页面路径
        #         'queryset':queryset
        #     }
        #     return JsonResponse(json_dict)


def admin_add(request):
    title = '新建管理员页面'
    if request.method == 'GET':
        form = AdminModelForm()
        data_dict = {
            'status': True,
            'form': form,
            'title': title,
            'error': form.errors
                     }
        return JsonResponse(data_dict)
        #return render(request, 'change.html', {'from': form, 'title': title})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {
                'status': True,
                'url': 'admin/list/',#需跳转的页面路径
                'title': title,
                'error': form.errors
                         }
            return JsonResponse(data_dict)
        else:
            data_dict={
                'status':False,
                'error':form.errors
                       }
            return JsonResponse(data_dict,ensur_ascii=False)
    #return render(request, 'change.html', {'from': form, 'title': title})


def admin_edit(request, nid):
    title = '编辑管理员页面'
    object = models.Admin.objects.filter(id=nid).first()
    if request.method == 'GET':
        if not object:
            data_dict = {
                'status': False,
                'url': 'admin/list/',#需跳转的页面路径
                'title': title
                         }
            return JsonResponse(data_dict)
            #return redirect('admin_list.html')
        form = AdminModelForm(instance=object)
        return JsonResponse(form)
    if request.method == 'POST':
        form = AdminModelForm(data=request.POST,instance=object)
        if form.is_valid():
            form.save()
            data_dict={
                'status':True,
                'url':'admin/list/',#需跳转的页面路径
                'state':'编辑成功',
                'error': form.errors
                       }
            return JsonResponse(data_dict)
    #return render(request, 'change.html', {'from': form, 'title': title})


def admin_delete(request,nid):
    models.Admin.objects.filter(id=nid).delete()
    data_dict = {
        'status': True,
        'url':'admin/list/',#需跳转的页面路径
    }
    return JsonResponse(data_dict)


def admin_reset(request,nid):
    object=models.Admin.objects.filter(id=nid).first()
    if not object:
        data_dict = {
            'status': False,
            'url': 'admin/list/',#需跳转的页面路径
            'state':'该管理员不存在',
                    }
        return JsonResponse(data_dict)
        #return redirect('admin/list')
    title='重置密码——{}'.format(object.username)
    if request.method=='GET':
        form =AdminResetModelForm()
        data_dict = {
            'status': True,
            'form': form,
            'title': title,
            'error':form.errors
                     }
        return JsonResponse(data_dict)
        #return render(request,'change.html',{'title':title})
    if request.method=='POST':
        form = AdminResetModelForm(data=request.POST,instance=object)
        if form.is_valid():
            form.save()
            data_dict = {
                'status': True,
                'url': 'admin/list/',#需跳转的页面路径
                'state': '重置密码成功'
                         }
            return JsonResponse(data_dict)
        else:
            data_dict={
                'status': False,
                'error':form.errors
                       }
            return JsonResponse(data_dict,ensur_ascii=False)

            #return redirect('admin/list/')
        #return render(request, 'change.html', {'from': form, 'title': title})
