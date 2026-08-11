from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):

    def _create_user(self , username = None , email = None , password = None , **extra_fields):
        if username is None or email is None:
            raise ValueError("User must provide username and email")

        email = self.normalize_email(email)

        user = self.model(username = username , email = email , **extra_fields)

        user.set_password(password)

        user.save(using = self._db)

        return user

    def create_user(self , username = None , email = None , password = None , **extra_fields):
        extra_fields.setdefault("is_superuser" , False)

        extra_fields.setdefault("is_active" , True)

        return self._create_user(username = username , email = email , password =  password , **extra_fields)

    def create_superuser(self , username = None , email = None , password = None , **extra_fields):
        extra_fields.setdefault("is_superuser" , True)

        extra_fields.setdefault("is_staff" , True)


        extra_fields.setdefault("user_type" , CustomUser.UserTypeChoice.ADMIN)

        if extra_fields.get("is_superuser") != True:
            raise ValueError("Superuser must have is_superuser = True")

        if extra_fields.get("is_staff") != True:
                    raise ValueError("Superuser must have is_staff = True")

        if extra_fields.get("user_type") != CustomUser.UserTypeChoice.ADMIN:
            raise ValueError("Superuser must have user_type = Admin")

        return self._create_user(username = username , email = email , password =  password , **extra_fields)

class CustomUser(AbstractBaseUser , PermissionsMixin):
    id = models.UUIDField(primary_key = True , default = uuid.uuid4 , editable = False)

    first_name = models.CharField(max_length = 50)

    last_name = models.CharField(max_length = 50)

    username = models.CharField(max_length = 20 , unique = True)

    email = models.EmailField(unique = True)

    date_of_birth = models.DateField(blank = True , null = True)

    class UserTypeChoice(models.TextChoices):

        ADMIN = "admin" , "Admin"
        CUSTOMER = "customer" , "Customer"
        DELIVERY_AGENT = "delivery_agent" , "Delivery Agent"
        CUSTOMER_SUPPORT = "customer_support" , "Customer Support"

    user_type = models.CharField(max_length = 20 , choices = UserTypeChoice.choices , default = UserTypeChoice.CUSTOMER)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default = False)

    created_at = models.DateTimeField(auto_now_add = True)

    REQUIRED_FIELDS = ["email"]

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["user_type" , "-created_at"]

