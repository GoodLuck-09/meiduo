from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

# from mall.apps.users.models import User
# from apps.users.models import User
# from users.models import User
# 正确
from users.models import User
from users.serializers import RegiserUserSerializer

"""
1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.路由和请求方式
4.确定视图
5.按照步骤实现功能


 前端发送用户给后端 我们后端判断用户名 是否注册

 请求方式:
 GET        /users/usernames/(?P<username>\w{5,20})/count/

 # itcast 0
 # itcast 1

 POST


"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#ListAPIVIew,RetriveAPIView     封装好了

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class RegisterUsernameAPIView(APIView):

    def get(self,request,username):
        # 判断用户是否注册
        # 查询用户名的数量
        # itcast 0   没有注册
        # itcast 1   有注册

        count = User.objects.filter(username=username).count()

        # 返回数据
        return Response({'count':count,
                         'username':username})


"""

1.分析需求 (到底要干什么)
2.把需要做的事情写下来(把思路梳理清楚)
3.路由和请求方式
4.确定视图
5.按照步骤实现功能

当用户点击注册按钮的时候 前端需要收集     手机号,用户名,密码,短信验证码,确认密码,是否同意协议

1. 接收数据
2. 校验数据
3. 数据入库
4. 返回相应

POST    /users/register/



"""
#APIView                        基类
#GenericAPIVIew                 对列表视图和详情视图做了通用支持,一般和mixin配合使用
#CreateAPIView                  封装好了


class RegiserUserAPIView(APIView):

    def post(self,reqeust):
        # 1. 接收数据
        data = reqeust.data
        # 2. 校验数据
        serializer = RegiserUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. 数据入库
        serializer.save()



        # 4. 返回相应
        # 序列化: 将模型转换为JSON
        # 如何序列化的呢? 我们的序列化器是根据字段来查询模型中的对应数据,如果 序列化器中有 模型中没有,则会报错
        # 如果字段设置为 write_only 则会在 序列化中 忽略此字段
        return Response(serializer.data)



"""
当用户注册成功之后,自动登陆

自动登陆的功能 是要求 用户注册成功之后,返回数据的时候
需要额外添加一个 token

1. 序列化的时候 添加token
2. token 怎么生成

"""
