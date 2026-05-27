from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/new/', views.shipment_create, name='shipment_create'),
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment_detail'),
    path('shipments/<int:pk>/add-item/', views.shipment_add_item, name='shipment_add_item'),
    path(
        'shipments/<int:shipment_pk>/items/<int:item_pk>/delete/',
        views.shipment_delete_item,
        name='shipment_delete_item',
    ),
    path('about/', views.about, name='about'),
]
