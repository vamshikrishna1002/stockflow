from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=150)
    default_low_stock_threshold = models.PositiveIntegerField(default=5)  # FR-7
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Profile(models.Model):  # links user to org (FR-2)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    low_stock_threshold = models.PositiveIntegerField(null=True, blank=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('organization', 'sku')   # SKU unique per org
        ordering = ['name']

    @property
    def effective_threshold(self):
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold
        return self.organization.default_low_stock_threshold

    @property
    def is_low_stock(self):
        return self.quantity <= self.effective_threshold

    def __str__(self):
        return f'{self.name} ({self.sku})'