from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.template.loader import get_template

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import enquiry_tableSerializer
from .models import Product, BulkOrder, BulkOrderItem, enquiry_table
from .forms import ProductForm, BulkOrderForm, BulkOrderItemForm

from xhtml2pdf import pisa
import json


# -------------------- CUSTOM FILTER --------------------
from django import template
register = template.Library()

@register.filter(name='mul')
def multiply(value, arg):
    return value * arg


# -------------------- BASIC PAGES --------------------
def home(request):
    return render(request, 'index.html')

def aboutus(request):
    return render(request, 'about.html')

def problem_statement(request):
    return render(request, 'services.html')

def service(request):
    return render(request, 'services.html')

def freshness(request):
    return render(request, 'services/freshness.html')

def farming(request):
    return render(request, 'services/farming.html')

def delivery(request):
    return render(request, 'services/delivery.html')

def workshops(request):
    return render(request, 'services/workshops.html')

def recycle(request):
    return render(request, 'services/recycle.html')


# -------------------- CONTACT --------------------
def reg_form(request):
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('phone')
        d = request.POST.get('message')

        enquiry_table.objects.create(name=a, email=b, phone=c, message=d)

        messages.success(request, 'Enquiry Form Submitted Successfully...')

    return render(request, 'contact.html')


# -------------------- LOGIN --------------------
def login_user(request):

    next_url = request.GET.get('next')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # CASE 1: if coming from protected page (like bulk order)
            if next_url:
                return redirect(next_url)

            #  CASE 2: ADMIN LOGIN
            if user.is_superuser:
                return redirect('dashboard')   # your dashboard url

            # CASE 3: NORMAL USER
            return redirect('home')

        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')# -------------------- ADMIN ONLY --------------------
def admin_only(user):
    return user.is_superuser

@user_passes_test(admin_only, login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard/index.html')


# -------------------- ENQUIRY TABLE --------------------
@login_required(login_url='/login/')
def enquiry(request):
    data = enquiry_table.objects.all()
    return render(request, 'dashboard/tables.html', {'information': data})

@login_required(login_url='/login/')
def delete_record(request, id):
    if request.method == 'POST':
        enquiry_table.objects.get(pk=id).delete()
    return HttpResponseRedirect('/table/')

@login_required(login_url='/login/')
def edit_record(request, id):
    info = enquiry_table.objects.filter(pk=id)
    return render(request, 'dashboard/editrecord.html', {'information': info})

@login_required(login_url='/login/')
def update_record(request, id):
    info = enquiry_table.objects.get(pk=id)
    info.name = request.POST.get('name')
    info.email = request.POST.get('email')
    info.phone = request.POST.get('phone')
    info.message = request.POST.get('message')
    info.save()
    return HttpResponseRedirect('/table/')


# -------------------- LOGOUT --------------------
def logout_user(request):
    logout(request)
    return redirect('/')


# -------------------- API --------------------
class student_data(APIView):
    def get(self, request, format=None):
        data = enquiry_table.objects.all()
        serializer = enquiry_tableSerializer(data, many=True)
        return Response(serializer.data)


# -------------------- SIGNUP --------------------
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Signup successful! Please login.")
        return redirect('login')

    return render(request, 'signup.html')


# -------------------- STORE --------------------
@login_required(login_url='/login/')
def store(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# -------------------- ADD PRODUCT --------------------
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('store')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


# -------------------- BULK ORDER --------------------
@login_required(login_url='/login/')
def bulk_order(request):
    products = Product.objects.all()
    selected_items = request.session.get('selected_items', [])

    if request.method == "POST":

        if 'add_item' in request.POST:
            item_form = BulkOrderItemForm(request.POST)
            if item_form.is_valid():
                product = item_form.cleaned_data['product']
                quantity = item_form.cleaned_data['quantity']
                price = product.price_per_kg * quantity

                selected_items.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'quantity': quantity,
                    'price': float(price),
                })

                request.session['selected_items'] = selected_items
                return redirect('bulk_order')

        elif 'place_order' in request.POST:
            order_form = BulkOrderForm(request.POST)

            if order_form.is_valid():
                order = order_form.save()

                for item in selected_items:
                    BulkOrderItem.objects.create(
                        order=order,
                        product=Product.objects.get(id=item['product_id']),
                        quantity=item['quantity'],
                        price=item['price']
                    )

                request.session['selected_items'] = []
                return redirect('order_success', order_id=order.id)

    total_price = sum(item['price'] for item in selected_items) if selected_items else 0

    return render(request, "bulk_order.html", {
        "order_form": BulkOrderForm(),
        "item_form": BulkOrderItemForm(),
        "selected_items": selected_items,
        "total_price": total_price,
        "products": products,
    })


# -------------------- ORDER SUCCESS --------------------
def order_success(request, order_id):
    order = BulkOrder.objects.get(id=order_id)
    total_amount = sum(item.product.price_per_kg * item.quantity for item in order.bulkorderitem_set.all())

    return render(request, 'order_success.html', {
        'order': order,
        'total_amount': total_amount
    })


# -------------------- DOWNLOAD BILL --------------------
def download_bill(request, order_id):
    order = BulkOrder.objects.get(id=order_id)
    items = order.bulkorderitem_set.all()

    total_amount = sum(item.product.price_per_kg * item.quantity for item in items)

    template = get_template("bill_template.html")
    html = template.render({
        'order': order,
        'items': items,
        'total_amount': total_amount,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bill_Order_{order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response