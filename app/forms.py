"""Forms for the Nifty Gadgets application."""

from django import forms
from .models import Product, Review
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Optional. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')  # password fields are automatically included by UserCreationForm

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        if email:
            user.user_email = email
        else:
            # Generate a unique email if none provided
            user.user_email = f"user_{user.username}@niftygadgets.local"
        if commit:
            user.save()
        return user

class ProductForm(forms.ModelForm):
    """Form for adding a new product."""
    class Meta:
        model = Product
        fields = [
            'product_title',
            'product_description',
            'product_category',
            'product_price',
            'product_image',
            'product_link'
        ]
        widgets = {
            'product_title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'product_description': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 4}),
            'product_category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'product_price': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'step': '0.01'}),
            'product_image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            'product_link': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'https://example.com/product'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly make category required
        self.fields['product_category'].required = True

class ReviewForm(forms.ModelForm):
    """Form for adding a review."""
    class Meta:
        model = Review
        fields = ['review_title', 'review_score', 'review_content']
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'review_score': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'min': 1, 'max': 5}),
            'review_content': forms.Textarea(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'rows': 4})
        }
