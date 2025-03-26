from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Ensure we do not call `request.user` inside `authenticate()`
        auth_token = request.COOKIES.get("auth_token")

        if not auth_token:
            return None  # No authentication token found

        try:
            user = User.objects.get(auth_token=auth_token)
            return (user, None)
        except User.DoesNotExist:
            return None  # Invalid token

