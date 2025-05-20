"""Forms for the Nifty Gadgets application."""

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews."""
    class Meta:
        """Meta class for the ReviewForm."""
        model = Review
        fields = ['review_title', 'review_score', 'review_content']
        widgets = {
            'review_title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'review_score': forms.Select(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }, choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)]),
            'review_content': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 4
            })
        }
