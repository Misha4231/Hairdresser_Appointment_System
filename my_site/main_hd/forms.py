from django import forms
from .models import ReviewsModel

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = ReviewsModel
        fields = '__all__'