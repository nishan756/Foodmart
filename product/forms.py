from django import forms 
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ["user" , "product" , "created_at" , "is_active"]
        widgets = {
            "feedback":forms.Textarea(
                attrs = {
                    "type":"text",
                    "placeholder":"Your feedback",
                    "class":"form-control",
                    "rows":3,
                }
            )
        }