from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from catalog.models import Battery, BatteryType
from catalog.views import PRODUCT_SPECIALIST_GROUP, SALES_MANAGER_GROUP


PASSWORD = 'test-password-123'


def create_user(username, group_name=None, is_superuser=False):
    user_model = get_user_model()
    if is_superuser:
        return user_model.objects.create_superuser(
            username=username,
            email=f'{username}@example.com',
            password=PASSWORD,
        )

    user = user_model.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password=PASSWORD,
    )
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
    return user


def create_product_specialist(username='specialist'):
    return create_user(username, PRODUCT_SPECIALIST_GROUP)


def create_sales_manager(username='manager'):
    return create_user(username, SALES_MANAGER_GROUP)


def create_battery_type(name='Автомобильный', slug='car'):
    return BatteryType.objects.create(
        name=name,
        slug=slug,
        description='Тестовый тип аккумуляторов.',
    )


def create_battery(battery_type=None, **overrides):
    if battery_type is None:
        battery_type = create_battery_type()

    data = {
        'sku': 'AKB-TEST-001',
        'name': 'Test Battery 60Ah',
        'brand': 'TestBrand',
        'battery_type': battery_type,
        'capacity_mah': 60000,
        'voltage_v': '12.00',
        'starting_current_a': 540,
        'weight_grams': 14500,
        'price': '6500.00',
        'small_wholesale_price': '6200.00',
        'small_wholesale_min_quantity': 5,
        'large_wholesale_price': '5900.00',
        'large_wholesale_min_quantity': 20,
        'stock_quantity': 4,
        'warranty_months': 24,
        'description': 'Тестовый аккумулятор.',
    }
    data.update(overrides)
    return Battery.objects.create(**data)


def battery_form_data(battery_type, **overrides):
    data = {
        'sku': 'AKB-FORM-001',
        'name': 'Form Battery',
        'brand': 'FormBrand',
        'battery_type': str(battery_type.pk),
        'capacity_mah': '60000',
        'voltage_v': '12.00',
        'starting_current_a': '540',
        'weight_grams': '14500',
        'price': '6500.00',
        'small_wholesale_price': '6200.00',
        'small_wholesale_min_quantity': '5',
        'large_wholesale_price': '5900.00',
        'large_wholesale_min_quantity': '20',
        'stock_quantity': '4',
        'warranty_months': '24',
        'fast_charge': '',
        'description': 'Описание из формы.',
    }
    data.update(overrides)
    return data
