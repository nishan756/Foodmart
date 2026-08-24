from django import forms 

from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user" , "total_price" , "status" , "created_at" , "shipped_at"]


    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)

        for name , field in self.fields.items():

            field.widget.attrs.update({"class":"form-control" , "placeholder":name.replace("_" , " ").title() , "disabled":True if name == "full_name" or name == "email" else False , "id":name})

            field.label_suffix = ""
