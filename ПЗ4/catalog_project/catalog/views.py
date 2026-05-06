from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Battery, BatteryType


def product_list(request):
    products = Battery.objects.select_related('battery_type')
    query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('type', '').strip()
    selected_availability = request.GET.get('availability', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(sku__icontains=query)
            | Q(description__icontains=query)
        )

    if selected_type:
        products = products.by_type(selected_type)

    if selected_availability == 'in_stock':
        products = products.in_stock()
    elif selected_availability == 'out_of_stock':
        products = products.filter(stock_quantity=0)

    context = {
        'products': products,
        'battery_types': BatteryType.objects.all(),
        'query': query,
        'selected_type': selected_type,
        'selected_availability': selected_availability,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Battery.objects.select_related('battery_type'), pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def about(request):
    return render(request, 'catalog/about.html')
