from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from mall import settings


def generic_verify_url(user_id):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    data = {'id': user_id}
    token = s.dumps(data)

    url = 'www.meiduo.site:8080/success_verify_email.html?token='
    return url + token.decode()


def check_token(token):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    try:
        res = s.loads(token)
    except BadSignature:

        return None

    return res.get('id')



