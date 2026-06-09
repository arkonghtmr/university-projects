from django.test import TestCase

from catalog.forms import BatteryForm
from catalog.models import Battery
from catalog.tests.helpers import battery_form_data, create_battery, create_battery_type


# Тесты формы проверяют бизнес-правила для создания и редактирования товара.
class BatteryFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Тип аккумулятора нужен форме как обязательный внешний ключ.
        cls.battery_type = create_battery_type()

    def test_battery_form_accepts_valid_product_data(self):
        # Корректно заполненная форма должна проходить валидацию.
        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertTrue(form.is_valid(), form.errors)

    def test_battery_form_creates_product(self):
        # После save() валидная форма создает запись Battery в тестовой БД.
        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertTrue(form.is_valid(), form.errors)
        product = form.save()

        self.assertEqual(product.sku, 'AKB-FORM-001')
        self.assertEqual(Battery.objects.count(), 1)

    def test_battery_form_rejects_duplicate_sku(self):
        # Артикул sku уникален, поэтому повторное значение должно дать ошибку поля.
        create_battery(self.battery_type, sku='AKB-FORM-001')

        form = BatteryForm(data=battery_form_data(self.battery_type))

        self.assertFalse(form.is_valid())
        self.assertIn('sku', form.errors)

    def test_battery_form_rejects_small_wholesale_price_above_unit_price(self):
        # Мелкооптовая цена не может быть выше розничной цены за единицу.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                small_wholesale_price='7000.00',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('small_wholesale_price', form.errors)

    def test_battery_form_rejects_large_wholesale_price_above_small_wholesale_price(self):
        # Крупнооптовая цена не должна быть выше мелкооптовой.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                large_wholesale_price='6300.00',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('large_wholesale_price', form.errors)

    def test_battery_form_rejects_large_wholesale_quantity_not_greater_than_small(self):
        # Порог крупного опта должен быть больше порога мелкого опта.
        form = BatteryForm(
            data=battery_form_data(
                self.battery_type,
                large_wholesale_min_quantity='5',
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn('large_wholesale_min_quantity', form.errors)
