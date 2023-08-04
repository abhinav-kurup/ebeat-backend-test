# from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the user from the Django session
        user = request.user

        if user and user.is_authenticated:
            return user, None
        else:
            raise AuthenticationFailed('No active session found.')