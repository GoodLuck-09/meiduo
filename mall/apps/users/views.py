from rest_framework import status
from rest_framework.response import Response
from users.models import User
from users.serializers import RegiserUserSerializer, UserCenterInfoSerializer, UserEmailInfoSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from users.utils import check_token


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


class UserCenterInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserCenterInfoSerializer(user)

        return Response(serializer.data)


class UserEmailInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        data = request.data

        serializer = UserEmailInfoSerializer(instance=request.user, data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)


class UserVerifyEmailAPIView(APIView):
    def get(self, request):
        data = request.query_params
        token = data.get('token')
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 解析token

        user_id =  check_token(token)
        user = User.objects.get(pk=user_id)

        user.email_active = True
        user.save()

        return Response({"msg":'ok'})





