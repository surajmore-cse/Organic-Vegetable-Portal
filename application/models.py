from django.db import models

class enquiry_table(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure this field exists
    description = models.TextField()

    def __str__(self):
        return self.name

class BulkOrder(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    products = models.ManyToManyField('Product', through='BulkOrderItem')  
    payment_method = models.CharField(max_length=20, choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')])
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name}"

class BulkOrderItem(models.Model):
    order = models.ForeignKey(BulkOrder, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Set default value here

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"




class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Use string reference 'Order'
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for order {self.order.id}"

