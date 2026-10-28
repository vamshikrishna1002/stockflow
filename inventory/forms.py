from django import forms
from django.contrib.auth.models import User
from .models import Organization, Product


class SignupForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    organization_name = forms.CharField(max_length=150)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'quantity', 'cost_price',
                  'selling_price', 'low_stock_threshold']

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.organization = organization

    def clean_sku(self):
        sku = self.cleaned_data['sku'].strip()
        qs = Product.objects.filter(organization=self.organization, sku__iexact=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('This SKU already exists in your organization.')
        return sku


class AdjustStockForm(forms.Form):
    change = forms.IntegerField(label='+/- units')
    note = forms.CharField(max_length=200, required=False)


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['default_low_stock_threshold']