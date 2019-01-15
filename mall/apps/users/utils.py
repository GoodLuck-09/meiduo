from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mall import settings

def generic_verify_url(user_id):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    data = {'id': user_id}
    token = s.dumps(data)

    url = 'www.meiduo.site:8080/success_verify_email.html?token='
    return url + token.decode()



