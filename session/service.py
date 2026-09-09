from .repository import UserRepo , User
from django.db.models import Q
from core.exceptions import ObjectAlreadyExists
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UserService:
    repo = UserRepo()

    def create_user(self , validated_data):

        if User.objects.filter(username = validated_data.get("username")).exists():
            raise ObjectAlreadyExists("User with this username is already exists")

        if User.objects.filter(email = validated_data.get("email")).exists():
            raise ObjectAlreadyExists("User with this username is already exists")

        validated_data.pop("password2")

        validated_data["password"] = validated_data.pop("password1")
        return self.repo.create_user(**validated_data)

    def user_delete(self , user):
        return self.repo.user_delete(user)

    def change_password(self , user , old_password , new_password):
        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect")

        validate_password(new_password , user)
        user.set_password(new_password)
        user.save()
        return 