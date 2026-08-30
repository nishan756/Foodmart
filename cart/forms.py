from django import forms 

from .models import Order

class OrderForm(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)
    
        for name , field in self.fields.items():
    
            field.widget.attrs.update({"class":"form-control" , "placeholder":name.replace("_" , " ").title()})
    
            field.label_suffix = ""
            
    class Meta:
        model = Order
        exclude = ["user" , "total_price" , "status" , "created_at" , "shipped_at" , "shipping_charge"]

class OrderFilterForm(forms.Form):
    date_from = forms.DateField(
        widget = forms.DateInput(attrs = {"type":"date"}),
    )
    date_to = forms.DateField(
        widget = forms.DateInput(attrs = {"type":"date"})
    )

    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)

        for name , field in self.fields.items():
            field.widget.attrs.update({"class":"form-control" , "id":name})
            field.label_suffix = ""

