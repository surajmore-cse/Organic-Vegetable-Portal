from django.contrib import admin

from .models import enquiry_table, Product

# Register your models here.

admin.site.register(enquiry_table) 

admin.site.register(Product)