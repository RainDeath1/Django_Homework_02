from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None
        try:
            token = header.split(' ')[1]
            decoded_token = AccessToken(token)
            decoded_token.check_exp()
        except Exception as e:
            raise exceptions.AuthenticationFailed('Неверный токен')
        user = decoded_token['user_id']
        return (user, None)
