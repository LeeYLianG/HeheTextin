import requests
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleware(MiddlewareMixin):
    def process_requests(self,request):
        if request.path_info=='/login/':
            return
        #读取当前访问用户的session信息，如果能读到，说民已经登录，可以继续向后
        info_dict=requests.session().get('info')
        if info_dict:
            return
        #当前用户没有登录没有登录
        else:
            return redirect('/login/')