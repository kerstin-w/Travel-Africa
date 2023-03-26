from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CaseInsensitiveModelBackend(ModelBackend):
    """
    Custom Authentication Backend to handle case-insenstive username
    for login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
