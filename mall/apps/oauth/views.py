from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from mall import settings
from rest_framework import status

from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import generic_open_id


class OAuthQQURLAPIView(APIView):

    def get(self,request):


        # auth_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101474184&redirect_uri=http://www.meiduo.site:8080/oauth_callback.html&state=test'
        #成功之后 回调到哪里去
        state = '/'
        #1.创建oauthqq的实例对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)

        #2. 获取跳转的url
        auth_url = oauth.get_qq_url()

        return Response({'auth_url':auth_url})


class OAuthQQUserAPIView(APIView):

    def get(self,request):
        # 1. 接收这个数据
        params = request.query_params
        code = params.get('code')
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 2. 用code换token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        token = oauth.get_access_token(code)
        # '336DAF004732E4FB403B7C0FBE9C33DE'
        # 3. 用token换openid
        openid = oauth.get_open_id(token)

        #openid是此网站上唯一对应用户身份的标识，网站可将此ID进行存储便于用户下次登录时辨识其身份
        # 获取的openid有两种情况:
        # 1. 用户之前绑定过
        # 2. 用户之前没有绑定过

        # 根据openid查询数据
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            #不存在

            # openid 很重要 ,所以我们需要对openid进行一个处理

            token = generic_open_id(openid)

            return  Response({'access_token':token})

        else:
            # 存在,应该让用户登陆

            from rest_framework_jwt.settings import api_settings

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(qquser.user)
            token = jwt_encode_handler(payload)

            return Response({
                'token':token,
                'username':qquser.user.username,
                'user_id':qquser.user.id
            })

    def post(self,request):
        # 1. 接收数据
        data = request.data
        # 2. 对数据进行校验
        serializer = OAuthQQUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3. 保存数据
        qquser = serializer.save()
        # 4. 返回相应, 应该有token数据

        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(qquser.user)
        token = jwt_encode_handler(payload)

        return Response({
            'token': token,
            'username': qquser.user.username,
            'user_id': qquser.user.id
        })


