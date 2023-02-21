"""textin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from hehe.views import users,consume,admin,account



urlpatterns = [
    #消费管理
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    path('consume/list/',consume.ListView.as_view()),
    path('consume/scan/',consume.consumeScan),
    path('consume/add/',consume.addView),
    path('consume/edit/',consume.editView),
    #path('admin/', admin.site.urls),

    #用户管理
    path('users/login/', users.loginView),
    path('users/register/',users.registerView),
    path('users/<int:nid>/edit/',users.user_edit),


    #管理员
    path('admin/list',admin.adminView),
    path('admin/add',admin.admin_add),
    path('admin/<int:nid>/edit',admin.admin_edit),
    path('admin/<int:nid>/delete',admin.admin_delete),
    path('admin/<int:nid>/reset',admin.admin_reset),


    #登录
    path('login/',account.login),
    path('logout/',account.logout),

]
