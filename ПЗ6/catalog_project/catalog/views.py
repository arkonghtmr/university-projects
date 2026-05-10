from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BatteryForm, ShipmentForm, ShipmentItemForm
from .models import Battery, BatteryType, Shipment, ShipmentItem


PRODUCT_SPECIALIST_GROUP = 'Товароведы'
SALES_MANAGER_GROUP = 'Менеджеры продаж'


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


def is_product_specialist(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=PRODUCT_SPECIALIST_GROUP).exists()
    )


def is_sales_manager(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=SALES_MANAGER_GROUP).exists()
    )


def role_required(check):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not check(request.user):
                return HttpResponseForbidden('Недостаточно прав для выполнения операции.')
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def role_context(request):
    return {
        'can_manage_products': is_product_specialist(request.user),
        'can_manage_shipments': is_sales_manager(request.user),
    }


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

    context = role_context(request) | {
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
    return render(request, 'catalog/product_detail.html', role_context(request) | {'product': product})


@role_required(is_product_specialist)
def product_create(request):
    if request.method == 'POST':
        form = BatteryForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect(product)
    else:
        form = BatteryForm()

    context = role_context(request) | {
        'form': form,
        'title': 'Добавить аккумулятор',
        'submit_label': 'Создать товар',
    }
    return render(request, 'catalog/product_form.html', context)


@role_required(is_product_specialist)
def product_update(request, pk):
    product = get_object_or_404(Battery, pk=pk)
    if request.method == 'POST':
        form = BatteryForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect(product)
    else:
        form = BatteryForm(instance=product)

    context = role_context(request) | {
        'form': form,
        'product': product,
        'title': 'Редактировать аккумулятор',
        'submit_label': 'Сохранить изменения',
    }
    return render(request, 'catalog/product_form.html', context)


@role_required(is_product_specialist)
def product_delete(request, pk):
    product = get_object_or_404(Battery, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    context = role_context(request) | {'product': product}
    return render(request, 'catalog/product_confirm_delete.html', context)


def get_allowed_shipment_or_404(request, pk):
    queryset = Shipment.objects.select_related('owner').prefetch_related('items__product')
    shipment = get_object_or_404(queryset, pk=pk)
    if not shipment.can_be_changed_by(request.user):
        return None
    return shipment


@role_required(is_sales_manager)
def shipment_list(request):
    shipments = Shipment.objects.select_related('owner').prefetch_related('items__product')
    if not request.user.is_superuser:
        shipments = shipments.filter(owner=request.user)

    return render(request, 'catalog/shipment_list.html', role_context(request) | {'shipments': shipments})


@role_required(is_sales_manager)
def shipment_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    shipment = Shipment.objects.create(owner=request.user)
    return redirect('shipment_detail', pk=shipment.pk)


@role_required(is_sales_manager)
def shipment_detail(request, pk):
    shipment = get_allowed_shipment_or_404(request, pk)
    if shipment is None:
        return HttpResponseForbidden('Эта партия принадлежит другому менеджеру.')

    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect('shipment_detail', pk=shipment.pk)
    else:
        form = ShipmentForm(instance=shipment)

    context = role_context(request) | {
        'shipment': shipment,
        'form': form,
        'item_form': ShipmentItemForm(),
    }
    return render(request, 'catalog/shipment_detail.html', context)


@role_required(is_sales_manager)
def shipment_add_item(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    shipment = get_allowed_shipment_or_404(request, pk)
    if shipment is None:
        return HttpResponseForbidden('Эта партия принадлежит другому менеджеру.')

    form = ShipmentItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.shipment = shipment
        item.save()

    return redirect('shipment_detail', pk=shipment.pk)


@role_required(is_sales_manager)
def shipment_delete_item(request, shipment_pk, item_pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    shipment = get_allowed_shipment_or_404(request, shipment_pk)
    if shipment is None:
        return HttpResponseForbidden('Эта партия принадлежит другому менеджеру.')

    item = get_object_or_404(ShipmentItem, pk=item_pk, shipment=shipment)
    item.delete()
    return redirect('shipment_detail', pk=shipment.pk)


def about(request):
    return render(request, 'catalog/about.html', role_context(request))
