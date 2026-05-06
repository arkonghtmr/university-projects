from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Battery, BatteryType


class BatteryValidationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.battery_type = BatteryType.objects.create(
            name='Автомобильный',
            slug='car',
            description='Стартерные аккумуляторы для легковых автомобилей.',
        )

    def setUp(self):
        self.valid_data = {
            'sku': 'AKB-TEST-001',
            'name': 'Test Battery 60Ah',
            'brand': 'TestBrand',
            'battery_type': self.battery_type,
            'capacity_mah': 60000,
            'voltage_v': Decimal('12.00'),
            'starting_current_a': 540,
            'weight_grams': 14500,
            'price': Decimal('6500.00'),
            'stock_quantity': 5,
            'warranty_months': 24,
            'fast_charge': False,
            'description': 'Тестовый аккумулятор.',
        }

    def build_battery(self, **overrides):
        return Battery(**(self.valid_data | overrides))

    def test_price_must_be_positive(self):
        battery = self.build_battery(price=Decimal('0.00'))

        with self.assertRaises(ValidationError) as context:
            battery.full_clean()

        self.assertIn('price', context.exception.message_dict)

    def test_capacity_must_be_positive(self):
        battery = self.build_battery(capacity_mah=0)

        with self.assertRaises(ValidationError) as context:
            battery.full_clean()

        self.assertIn('capacity_mah', context.exception.message_dict)

    def test_weight_can_be_empty_but_not_zero(self):
        battery_without_weight = self.build_battery(weight_grams=None)
        battery_without_weight.full_clean()

        battery_with_zero_weight = self.build_battery(weight_grams=0)
        with self.assertRaises(ValidationError) as context:
            battery_with_zero_weight.full_clean()

        self.assertIn('weight_grams', context.exception.message_dict)

    def test_sku_must_be_unique(self):
        Battery.objects.create(**self.valid_data)
        duplicate = self.build_battery(name='Duplicate Battery')

        with self.assertRaises(ValidationError) as context:
            duplicate.full_clean()

        self.assertIn('sku', context.exception.message_dict)

    def test_sku_allows_only_expected_characters(self):
        battery = self.build_battery(sku='акб-001')

        with self.assertRaises(ValidationError) as context:
            battery.full_clean()

        self.assertIn('sku', context.exception.message_dict)


class BatteryRelationTests(TestCase):
    fixtures = ['battery_catalog.json']

    def test_type_reverse_relation_returns_related_batteries(self):
        car_type = BatteryType.objects.get(slug='car')

        self.assertEqual(car_type.batteries.count(), 1)
        self.assertEqual(car_type.batteries.first().sku, 'AKB-VARTA-D24')

    def test_type_delete_is_protected_when_products_exist(self):
        car_type = BatteryType.objects.get(slug='car')

        with self.assertRaises(ProtectedError):
            car_type.delete()


class BatteryPropertyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.battery_type = BatteryType.objects.create(name='Power bank', slug='power-bank')

    def make_battery(self, **overrides):
        data = {
            'sku': 'AKB-PROP-001',
            'name': 'Property Battery',
            'brand': 'PropBrand',
            'battery_type': self.battery_type,
            'capacity_mah': 20000,
            'voltage_v': Decimal('3.70'),
            'weight_grams': 450,
            'price': Decimal('2500.00'),
            'stock_quantity': 2,
        }
        return Battery(**(data | overrides))

    def test_is_heavy_property(self):
        light_battery = self.make_battery(weight_grams=4999)
        heavy_battery = self.make_battery(sku='AKB-PROP-002', weight_grams=5000)

        self.assertFalse(light_battery.is_heavy)
        self.assertTrue(heavy_battery.is_heavy)

    def test_is_high_capacity_property(self):
        regular_battery = self.make_battery(capacity_mah=19999)
        high_capacity_battery = self.make_battery(sku='AKB-PROP-003', capacity_mah=20000)

        self.assertFalse(regular_battery.is_high_capacity)
        self.assertTrue(high_capacity_battery.is_high_capacity)


class BatteryManagerTests(TestCase):
    fixtures = ['battery_catalog.json']

    def test_by_type_manager_filters_by_slug(self):
        products = Battery.objects.by_type('power-bank')

        self.assertEqual(products.count(), 1)
        self.assertEqual(products.get().sku, 'AKB-XIAOMI-20000')

    def test_in_stock_manager_excludes_empty_stock(self):
        products = Battery.objects.in_stock()

        self.assertTrue(products.filter(sku='AKB-VARTA-D24').exists())
        self.assertFalse(products.filter(sku='AKB-GP-AA-2500').exists())

    def test_heavy_manager_returns_heavy_batteries(self):
        products = Battery.objects.heavy()

        self.assertTrue(products.filter(sku='AKB-VARTA-D24').exists())
        self.assertFalse(products.filter(sku='AKB-XIAOMI-20000').exists())


class BatteryConstraintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.battery_type = BatteryType.objects.create(name='ИБП', slug='ups')

    def setUp(self):
        self.valid_data = {
            'sku': 'AKB-DB-001',
            'name': 'DB Constraint Battery',
            'brand': 'DBBrand',
            'battery_type': self.battery_type,
            'capacity_mah': 9000,
            'voltage_v': Decimal('12.00'),
            'weight_grams': 2600,
            'price': Decimal('4300.00'),
            'stock_quantity': 1,
            'warranty_months': 12,
        }

    def test_db_check_constraint_rejects_negative_price(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Battery.objects.create(**(self.valid_data | {'price': Decimal('-1.00')}))

    def test_db_check_constraint_rejects_zero_capacity(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Battery.objects.create(**(self.valid_data | {'sku': 'AKB-DB-002', 'capacity_mah': 0}))

    def test_db_unique_constraint_rejects_duplicate_sku(self):
        Battery.objects.create(**self.valid_data)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Battery.objects.create(**(self.valid_data | {'name': 'Duplicate DB Battery'}))


class CatalogViewTests(TestCase):
    fixtures = ['battery_catalog.json']

    def test_product_list_page_is_accessible(self):
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.status_code, 200)

    def test_product_list_reads_products_from_database(self):
        response = self.client.get(reverse('product_list'))

        self.assertContains(response, 'VARTA Blue Dynamic D24')
        self.assertContains(response, 'AKB-XIAOMI-20000')

    def test_product_detail_reads_product_from_database(self):
        product = Battery.objects.get(sku='AKB-VARTA-D24')

        response = self.client.get(reverse('product_detail', args=[product.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.description)
        self.assertContains(response, '540 А')

    def test_product_detail_returns_404_for_missing_product(self):
        response = self.client.get(reverse('product_detail', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_search_filters_products(self):
        response = self.client.get(reverse('product_list'), {'q': 'VARTA'})

        self.assertContains(response, 'VARTA Blue Dynamic D24')
        self.assertNotContains(response, 'Xiaomi Redmi Power Bank 20000')

    def test_type_filter_filters_products(self):
        response = self.client.get(reverse('product_list'), {'type': 'aa-aaa'})

        self.assertContains(response, 'GP ReCyko AA 2500')
        self.assertNotContains(response, 'VARTA Blue Dynamic D24')
