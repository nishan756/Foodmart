from django.db import models
from django.contrib.auth import get_user_model 
from django.core.exceptions import ValidationError


User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , blank = True , null = True)

    session_id = models.CharField(max_length = 32 , blank = True , null = True , unique = True)

    created_at = models.DateTimeField(auto_now_add = True)

    def clean(self):
        if not self.user and not self.session_id:
            raise ValidationError(message = "User or session id required")

    def __str__(self):
        return f"Cart of {self.user}" if self.user else self.session_id

    class Meta:
        ordering = ["-created_at"]    