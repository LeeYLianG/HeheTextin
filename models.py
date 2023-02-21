from django.db import models

# Create your models here.
#消费列表
class Consume(models.Model):
    money=models.DecimalField(verbose_name='金额', max_digits=10,decimal_places=2)
    date=models.DateTimeField(verbose_name='时间',auto_now_add=True)
    no=models.CharField(verbose_name='单号',max_length=100,null=True,blank=True)
    shop=models.CharField(verbose_name='商户',max_length=200)
    shop_no=models.CharField(verbose_name='商户编号',max_length=100,null=True,blank=True)
    sku=models.CharField(verbose_name='商品',max_length=300)
    status_choice=(
        (1,'已支付'),
        (2,'未支付'),
    )
    status=models.SmallIntegerField(verbose_name='支付状态',choices=status_choice,default=1)
    consumer=models.ForeignKey(verbose_name='消费者',to='User',on_delete = models.CASCADE)
    picture = models.OneToOneField(verbose_name='上传图片', to='Image', on_delete=models.CASCADE)

#object=Consume()
class Image(models.Model):
    img=models.CharField(verbose_name='上传图片',max_length=128)



#用户列表
class User(models.Model):
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱', null=True,blank=True)
    phone = models.CharField(max_length=11, verbose_name='手机号码')

#管理员列表
class Admin(models.Model):
    username=models.CharField(verbose_name='用户名',max_length=32)
    password=models.CharField(verbose_name='密码',max_length=64)