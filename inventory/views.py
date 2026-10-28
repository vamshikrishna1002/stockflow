from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdjustStockForm, ProductForm, SettingsForm, SignupForm
from .models import Organization, Product, Profile


def get_org(request):
    return request.user.profile.organization


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            org = Organization.objects.create(name=form.cleaned_data['organization_name'])
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            Profile.objects.create(user=user, organization=org)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    org = get_org(request)
    products = Product.objects.filter(organization=org).select_related('organization')
    total_products = products.count()
    total_units = products.aggregate(t=Sum('quantity'))['t'] or 0
    low_stock = [p for p in products if p.is_low_stock]
    return render(request, 'inventory/dashboard.html', {
        'total_products': total_products,
        'total_units': total_units,
        'low_stock': low_stock,
    })


@login_required
def product_list(request):
    products = Product.objects.filter(organization=get_org(request)).select_related('organization')
    return render(request, 'inventory/product_list.html', {'products': products})


@login_required
def product_create(request):
    org = get_org(request)
    form = ProductForm(request.POST or None, organization=org)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.organization = org
        product.last_updated_by = request.user
        product.save()
        messages.success(request, 'Product created.')
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_update(request, pk):
    org = get_org(request)
    product = get_object_or_404(Product, pk=pk, organization=org)
    form = ProductForm(request.POST or None, instance=product, organization=org)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.last_updated_by = request.user
        product.save()
        messages.success(request, 'Product updated.')
        return redirect('product_list')
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, organization=get_org(request))
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


@login_required
def adjust_stock(request, pk):
    product = get_object_or_404(Product, pk=pk, organization=get_org(request))
    form = AdjustStockForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product.quantity = F('quantity') + form.cleaned_data['change']
        product.last_updated_by = request.user
        product.save()
        messages.success(request, 'Stock adjusted.')
        return redirect('product_list')
    return render(request, 'inventory/adjust_stock.html', {'form': form, 'product': product})


@login_required
def settings_view(request):
    org = get_org(request)
    form = SettingsForm(request.POST or None, instance=org)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Settings saved.')
        return redirect('settings')
    return render(request, 'inventory/settings.html', {'form': form})