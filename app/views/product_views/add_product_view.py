"""Add product view."""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import ProductCategory
from app.forms import ProductForm

@login_required
def add_product_view(request):
    """View for adding a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author_user = request.user
            product.save()

            # Update user's total entries
            request.user.total_entries_by_user += 1
            request.user.save(update_fields=['total_entries_by_user'])

            messages.success(request, 'Product added successfully!')
            return redirect('app:product_detail', product_id=product.product_id)
    else:
        form = ProductForm()

    context = {
        'form': form,
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'app/add_product.html', context)
