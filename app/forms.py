from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews."""
    class Meta:
        model = Review
        fields = ['review_title', 'review_score', 'review_content']
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'}),
            'review_score': forms.NumberInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'min': 1,
                'max': 5
            }),
            'review_content': forms.Textarea(attrs={
                'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full',
                'rows': 4
            }),
        }
