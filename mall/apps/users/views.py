from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import RegisterCreateSerializer


class RegisterUsernameCountAPIView(APIView):
    """
    获取用户名的个数
    GET:  /users/usernames/(?P<username>\w{5,20})/count/
    """

    def get(self,request,username):

        #通过模型查询,获取用户名个数
        count = User.objects.filter(username=username).count()
        #组织数据
        context = {
            'count':count,
            'username':username
        }
        return Response(context)


class RegisterPhoneCountAPIView(APIView):
    """
    查询手机号的个数
    GET: /users/phones/(?P<mobile>1[345789]\d{9})/count/
    """
    def get(self,request,mobile):

        #通过模型查询获取手机号个数
        count = User.objects.filter(mobile=mobile).count()
        #组织数据
        context = {
            'count':count,
            'phone':mobile
        }

        return Response(context)


# class RegisterCreateView(CreateAPIView):
class RegisterCreateView(APIView):
    """
    用户注册
    POST /users/

    用户注册我们需要对数据进行校验,同时需要数据入库
    """

    # serializer_class = RegisterCreateSerializer
    def post(self, request):

        data = request.data
        print(data)
        serializer = RegisterCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
