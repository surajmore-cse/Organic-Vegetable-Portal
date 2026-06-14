from django import forms
from .models import BulkOrder, BulkOrderItem, Product
from django.forms import formset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price_per_kg', 'description']
        
class BulkOrderForm(forms.ModelForm):
    class Meta:
        model = BulkOrder
        fields = ['customer_name', 'phone', 'address', 'payment_method']

class BulkOrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Select Product")
    quantity = forms.IntegerField(min_value=1, label="Quantity (Kg)")

    class Meta:
        model = BulkOrderItem
        fields = ['product', 'quantity']

# ✅ Formset should be defined after `BulkOrderItemForm`
BulkOrderItemFormSet = formset_factory(BulkOrderItemForm, extra=1)
