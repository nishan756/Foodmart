from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs = {
                "type":"text",
                "placeholder":"Username / Password",
                "required":True,
                "id":"username",
                "class":'form-control form-control-lg'
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
        attrs = {
            "placeholder":"Password",
            "required":True,
            "id":"password",
            "class":'form-control form-control-lg'
        }
    ))


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name , field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class":"form-control form-control-lg",
                    "placeholder":field_name.capitalize()
                }
            )
            field.label_suffix = " "
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name" , "last_name" , "username" , "email" , "date_of_birth"]

    