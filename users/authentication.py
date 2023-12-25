import contextlib
from django.contrib.auth import get_user_model, backends


class EmailAuthBackend(backends.BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        with contextlib.suppress(user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            """полученме пользователя по почте и сверка пароля"""
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
        return None
    
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
