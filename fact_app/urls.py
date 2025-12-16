from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('add_custumer',views.AddView.as_view(),name='add_customer'),
    path('add_invoice',views.AddInvoiceView.as_view(),name='add_invoice'),
    path('InvoiceDetailView/<int:pk>/',views.InvoiceDetailView.as_view(),name='InvoiceDetailView'),
    path('invoicepdf/<int:pk>/',views.get_invoice_pdf,name='invoice_pdf'),
    # path('post', views.post_view, name='post'), 
]

