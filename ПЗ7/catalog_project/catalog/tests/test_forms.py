from django.test import TestCase

from catalog.forms import BatteryForm
from catalog.models import Battery
from catalog.tests.helpers import battery_form_data, create_battery, create_battery_type


# Тесты формы проверяют создание товара и бизнес-валидацию цен/количеств.
class BatteryFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Тип аккумулятора нужен форме как обязательная связь товара с категорией.
        cls.battery_type = create_battery_type()

    def test_battery_form_accepts_valid_product_data(self):
        # Проверяет, что корректно заполненная форма проходит валидацию.
        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertTrue(form.is_valid(), form.errors)

    def test_battery_form_creates_product(self):
        # Проверяет, что валидная форма сохраняет новый товар в базу.
        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertTrue(form.is_valid(), form.errors)
        product = form.save()

        self.assertEqual(product.sku, 'AKB-FORM-001')
        self.assertEqual(Battery.objects.count(), 1)

    def test_battery_form_rejects_duplicate_sku(self):
        # Проверяет запрет дубля артикула: SKU должен быть уникальным.
        create_battery(self.battery_type, sku='AKB-FORM-001')

        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertFalse(form.is_valid())
        self.assertIn('sku', form.errors)

    def test_battery_form_rejects_small_wholesale_price_above_unit_price(self):
        # Проверяет, что мелкооптовая цена не может быть выше розничной.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                small_wholesale_price='7000.00',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('small_wholesale_price', form.errors)

    def test_battery_form_rejects_large_wholesale_price_above_small_wholesale_price(self):
        # Проверяет, что крупнооптовая цена не может быть выше мелкооптовой.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                large_wholesale_price='6300.00',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('large_wholesale_price', form.errors)

    def test_battery_form_rejects_large_wholesale_quantity_not_greater_than_small(self):
        # Проверяет, что порог крупного опта должен быть больше порога мелкого опта.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                large_wholesale_min_quantity='5',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('large_wholesale_min_quantity', form.errors)
