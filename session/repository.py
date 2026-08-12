from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class UserRepo:

    def create_user(self , **validated_data):
        user =  User.objects.create(**validated_data)
        user.set_password(validated_data.pop("password"))
        user.save(update_fields = ["password"])
        return user

    def user_delete(self , user):
        return user.delete()

    
