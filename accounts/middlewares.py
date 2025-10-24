from django.contrib.auth import get_user_model

User = get_user_model()


class UserMiddlewares:
    def getUserByEmailOrUsername(email, password):
        # Check against email and password
        try:
            user = User.objects.get(email=email)
            passcheck = user.check_password(password)
            return user if passcheck else False
        except User.DoesNotExist:
            return False