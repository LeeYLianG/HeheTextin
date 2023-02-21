import os
from django.conf import settings
from django import forms
from django.shortcuts import render
# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse
from django.core import serializers
from .. import models
from ..models import Consume
from django.utils.decorators import method_decorator
from ..utils.textin_scan import *
from ..models import Image


# ModelForm表单
class ConsunmeModelForm(forms.ModelForm):
    class Meta:
        model = models.Consume
        fields = '__all__'


class ListView(View):

    def get(self, request):
        data = models.Consume.objects.all()
        json_data = serializers.serialize('json', data)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        receive_data = json.loads(request.body.decode())
        money = receive_data['money']
        date = receive_data['date']
        no = receive_data['no']
        shop = receive_data['shop']
        shop_no = receive_data['shop_no']
        sku = receive_data['sku']
        status = receive_data['status']
        models.Consume.objects.create(money=money, date=date, no=no, shop=shop, shop_no=shop_no, sku=sku, status=status)
        post_data = {
            'money': money, 'date': date, 'no': no, 'shop': shop, 'shop_no': shop_no, 'sku': sku, 'status': status
        }
        return JsonResponse(data=post_data, json_dumps_params={'ensure_ascii': False})


def selectView(request, size):
    # 分页操作
    page = int(request.GET.get('page'))  # 分页
    page_size = size  # 每页显示数据量
    start = (page - 1) * page_size
    end = page * page_size
    # 搜索数据库所对应的数据库条件字典
    data_dict = {}
    # 搜索数据的各项条件（默认为空）既查询所有数据
    search_time = request.GET.get('date', '')
    max_money = request.GET.get('max', '')
    min_money = request.GET.get('min', '')
    goods = request.GET.get('sku', '')
    if search_time or max_money or min_money or goods:
        data_dict['date__contains'] = search_time
        data_dict['money__gte'] = min_money
        data_dict['money__lte'] = max_money
        data_dict['sku__contains'] = goods
    queryset = models.Consume.objects.filter(**data_dict).order_by('-date')[start:end]
    return JsonResponse(queryset, ensur_ascii=False)


def addView(request):
    # 新建消费
    title = '添加消费信息页面'
    if request.method == 'GET':
        form = ConsunmeModelForm()
        data_dict = {
            'status': True,
            'form': form,
            'title': title,
            'state': '获取添加页面'
        }
        return JsonResponse(data_dict, ensur_ascii=False)
        # return render(request, 'change.html', {'from': form, 'title': title})
    else:
        form = ConsunmeModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            data_dict = {
                'status': True,
                'url': 'consume/list/',  # 需跳转的页面路径
                'title': title,
                'state': '添加消费记录成功'
            }
            return JsonResponse(data_dict)
        else:
            data_dict = {
                'status': False,
                'error': form.errors,
                'state': '添加失败'
            }
            return JsonResponse(data_dict, ensur_ascii=False)


def deleteView(request):
    title = '删除消费信息'
    receive_data = json.loads(request.body.decode())  # 通过Json获取要删除的uid
    uid = receive_data['pk']
    # 删除记录
    # uid=request.GET.get('uid')#从前端获取删除item的uid
    exists_object = models.Consume.objects.filter(id=uid).exists()  # 将得到的uid与数据库的id匹配
    if not exists_object:
        data_dict = {
            'status': False,
            'title': title,
            'url': 'consume/list/',  # 需跳转的页面路径
            'error': '消费记录不存在'
        }
        return JsonResponse(data_dict)
    exists_object.delete()
    data_dict = {
        'status': True,
        'title': title,
        'url': 'consume/list/',  # 需跳转的页面路径
        'state': '删除成功'
    }
    return JsonResponse(data_dict)


def editView(request):
    title = '编辑消费信息'
    # uid = request.GET.get('uid')  # 从前端获取删除item的uid
    receive_data = json.loads(request.body.decode())  # 通过Json获取要删除的uid
    uid = receive_data['pk']
    exists_object = models.Consume.objects.filter(id=uid).first()
    if not exists_object:
        data_dict = {
            'status': False,
            'error': '编辑失败'
        }
        return JsonResponse(data_dict)
    form = ConsunmeModelForm(data=request.POST, instance=exists_object)
    if form.is_valid():
        form.save()
        data_dict = {
            'status': True,
            'form': form,
        }
        return JsonResponse(data_dict)
    else:
        data_dict = {
            'status': False,
            'error': form.errors
        }
        return JsonResponse(data_dict)



def consumeScan(request):
    title = '图片上传'
    if request.method == 'GET':
        data = models.Consume.objects.all()
        json_data = serializers.serialize('json', data)
        json_data = json.loads(json_data)
        return JsonResponse(data=json_data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        # if request.method=='POST' or request.method=='FILES':
        file_object = request.FILES.get('avatat')  # 获取的文件对象
        # f=open(file_object.name,mode='wb')
        # for chunk in file_object.chunks():
        #     f.write(chunk)
        # f.close()
        # receive_data = json.loads(request.body.decode())
        # image_object=receive_data['img']\
        search_path=os.path.join(settings.MEDIA_ROOT,file_object.name)
        media_path = os.path.join('media', file_object.name)
        # f = open(file_path, mode='wb')#将上传的文件以二进制写入静态文件
        # for chunk in file_object.chunks():
        #     f.write(chunk)
        # f.close()
        with open(media_path, "wb") as rfile:  # 将上传的文件以二进制写入静态文件img中
            data = file_object.file.read()
            rfile.write(data)  # 将文件内容写入rfile
        models.Image.objects.create(img=media_path)
        response = CommonOcr(search_path)  # 调用提供的方法，并将文件路径作为参数传入方法
        data_dict = {
            'status': True,
            'title': title,
            'response': response.recognize()
        }
        return JsonResponse(data_dict, safe=False, json_dumps_params={'ensure_ascii': False})
