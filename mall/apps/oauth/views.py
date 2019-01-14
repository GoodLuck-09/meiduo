from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from QQLoginTool.QQtool import OAuthQQ
from mall import settings
from rest_framework import status


class OAuthQQURLAPIView(APIView):

    def get(self, request):
        # 1创建oauth的实例
        state = 'test'
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)
        auth_url = oauth.get_qq_url()


        return Response({'auth_url': auth_url})


class OAuthQQUserAPIView(APIView):

    def get(self, request):
        data = request.query_params
        code = data['code']

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI
                        )

        token = oauth.get_access_token(code)

        open_id = oauth.get_open_id(token)

        pass



