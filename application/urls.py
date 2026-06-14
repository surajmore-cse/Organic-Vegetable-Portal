from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='Home'),
    path('aboutus/', views.aboutus, name='about'),
    path('problem_statement/', views.problem_statement, name='problem_statement'),
    path('services/', views.service, name='services'),
    path('services/freshness/', views.freshness, name='freshness'),
    path('services/farming/', views.farming, name='farming'),
    path('services/delivery/', views.delivery, name='delivery'),
    path('services/workshops/', views.workshops, name='workshops'),
    path('services/subscription/', views.recycle, name='recycle'),
    path('reg_form/', views.reg_form, name='reg'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('table/', views.enquiry, name='enq_tables'),
    path('delete/<int:id>/', views.delete_record, name='delete_record'),
    path('edit/<int:id>/', views.edit_record, name='edit_record'),
    path('update/<int:id>/', views.update_record, name='update_record'),
    path('logout/', views.logout_user, name='logout'),
    path('student_data', views.student_data.as_view(), name='student_data'),
    path('signup/', views.signup, name='signup'),
    path('add_product/', views.add_product, name='add_product'),
    path('store/', views.store, name='store'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('bulk_order/', views.bulk_order, name='bulk_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('download-bill/<int:order_id>/', views.download_bill, name='download_bill'),
]
