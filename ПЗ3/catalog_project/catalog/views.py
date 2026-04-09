from django.shortcuts import render

products_data = [
    {'id': 1, 'name': 'Автомобильный аккумулятор VARTA', 'desc': 'Емкость 60 Ач, пусковой ток 540 А, обратная полярность.', 'price': 6500},
    {'id': 2, 'name': 'Power Bank Xiaomi 20000mAh', 'desc': 'Портативный внешний аккумулятор с поддержкой быстрой зарядки.', 'price': 2500},
    {'id': 3, 'name': 'Аккумуляторные батарейки AA', 'desc': 'Комплект Ni-MH аккумуляторов, 4 штуки, емкость 2500 мАч.', 'price': 1200},
]

def product_list(request):
    return render(request, 'catalog/product_list.html', {'products': products_data})

def product_detail(request, pk):
    product = next((item for item in products_data if item['id'] == pk), None)
    return render(request, 'catalog/product_detail.html', {'product': product})

def about(request):
    return render(request, 'catalog/about.html')