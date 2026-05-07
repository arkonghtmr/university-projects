from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Battery, BatteryType


SORT_OPTIONS = {
    'name': {
        'label': 'По названию',
        'order_by': ('name',),
    },
    'price': {
        'label': 'По цене',
        'order_by': ('price', 'name'),
    },
    'weight': {
        'label': 'По весу',
        'order_by': ('weight_grams', 'name'),
    },
    'type': {
        'label': 'По типу',
        'order_by': ('battery_type__name', 'name'),
    },
}
DEFAULT_SORT = 'name'


def product_list(request):
    products = Battery.objects.select_related('battery_type')
    query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('type', '').strip()
    selected_availability = request.GET.get('availability', '').strip()
    selected_sort = request.GET.get('sort', DEFAULT_SORT).strip()

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

    if selected_sort not in SORT_OPTIONS:
        selected_sort = DEFAULT_SORT
    products = products.order_by(*SORT_OPTIONS[selected_sort]['order_by'])

    context = {
        'products': products,
        'battery_types': BatteryType.objects.all(),
        'query': query,
        'selected_type': selected_type,
        'selected_availability': selected_availability,
        'selected_sort': selected_sort,
        'sort_options': SORT_OPTIONS,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Battery.objects.select_related('battery_type'), pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def about(request):
    return render(request, 'catalog/about.html')
