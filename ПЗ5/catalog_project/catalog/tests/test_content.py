from django.test import TestCase
from django.urls import reverse

from catalog.models import Battery, BatteryType


class CatalogContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Общие тестовые данные для всех проверок содержимого каталога.
        car = BatteryType.objects.create(
            name='Автомобильный',
            slug='car',
            description='Стартерные аккумуляторы для легковых автомобилей.',
        )
        power_bank = BatteryType.objects.create(
            name='Power bank',
            slug='power-bank',
            description='Портативные внешние аккумуляторы для гаджетов.',
        )
        aa_aaa = BatteryType.objects.create(
            name='AA/AAA',
            slug='aa-aaa',
            description='Бытовые аккумуляторные элементы питания.',
        )
        ups = BatteryType.objects.create(
            name='ИБП',
            slug='ups',
            description='Аккумуляторы для источников бесперебойного питания.',
        )

        Battery.objects.create(
            sku='AKB-VARTA-D24',
            name='VARTA Blue Dynamic D24',
            brand='VARTA',
            battery_type=car,
            capacity_mah=60000,
            voltage_v='12.00',
            starting_current_a=540,
            weight_grams=14500,
            price='6500.00',
            stock_quantity=4,
            warranty_months=24,
            description='Автомобильный аккумулятор емкостью 60 Ач с пусковым током 540 А.',
        )
        Battery.objects.create(
            sku='AKB-XIAOMI-20000',
            name='Xiaomi Redmi Power Bank 20000',
            brand='Xiaomi',
            battery_type=power_bank,
            capacity_mah=20000,
            voltage_v='3.70',
            weight_grams=430,
            price='2500.00',
            stock_quantity=12,
            warranty_months=12,
            fast_charge=True,
            description='Портативный аккумулятор на 20000 мАч с поддержкой быстрой зарядки.',
        )
        Battery.objects.create(
            sku='AKB-GP-AA-2500',
            name='GP ReCyko AA 2500',
            brand='GP',
            battery_type=aa_aaa,
            capacity_mah=2500,
            voltage_v='1.20',
            weight_grams=120,
            price='1200.00',
            stock_quantity=0,
            warranty_months=6,
            description='Комплект из четырех Ni-MH аккумуляторов AA емкостью 2500 мАч.',
        )
        Battery.objects.create(
            sku='AKB-CSB-HRL1234',
            name='CSB HRL 1234W',
            brand='CSB',
            battery_type=ups,
            capacity_mah=9000,
            voltage_v='12.00',
            weight_grams=2600,
            price='4300.00',
            stock_quantity=3,
            warranty_months=18,
            description='Герметичный свинцово-кислотный аккумулятор для источников бесперебойного питания.',
        )

    def product_skus(self, response):
        # Возвращает артикулы товаров из контекста ответа в текущем порядке.
        return list(response.context['products'].values_list('sku', flat=True))

    def ordered_skus(self, *fields):
        # Возвращает ожидаемый порядок артикулов при сортировке по указанным полям.
        return list(Battery.objects.order_by(*fields).values_list('sku', flat=True))

    def test_product_list_uses_expected_template(self):
        # Список товаров должен использовать шаблон product_list.html.
        response = self.client.get(reverse('product_list'))

        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_product_list_context_contains_products_and_types(self):
        # View должна передавать в шаблон товары и типы аккумуляторов.
        response = self.client.get(reverse('product_list'))

        self.assertIn('products', response.context)
        self.assertIn('battery_types', response.context)
        self.assertEqual(response.context['products'].count(), 4)
        self.assertEqual(response.context['battery_types'].count(), 4)

    def test_product_list_renders_products_from_database(self):
        # На странице должны отображаться товары, созданные в тестовой базе.
        response = self.client.get(reverse('product_list'))

        self.assertContains(response, 'VARTA Blue Dynamic D24')
        self.assertContains(response, 'Xiaomi Redmi Power Bank 20000')

    def test_search_filters_products_by_query(self):
        # GET-параметр q должен оставлять только товары, подходящие под поиск.
        response = self.client.get(reverse('product_list'), {'q': 'VARTA'})

        self.assertContains(response, 'VARTA Blue Dynamic D24')
        self.assertNotContains(response, 'Xiaomi Redmi Power Bank 20000')
        self.assertEqual(self.product_skus(response), ['AKB-VARTA-D24'])

    def test_type_filter_shows_only_selected_group(self):
        # GET-параметр type должен фильтровать товары по типу аккумулятора.
        response = self.client.get(reverse('product_list'), {'type': 'aa-aaa'})

        self.assertContains(response, 'GP ReCyko AA 2500')
        self.assertNotContains(response, 'VARTA Blue Dynamic D24')
        self.assertEqual(self.product_skus(response), ['AKB-GP-AA-2500'])

    def test_availability_filter_shows_out_of_stock_products(self):
        # Фильтр out_of_stock должен показывать только товары без остатка.
        response = self.client.get(reverse('product_list'), {'availability': 'out_of_stock'})

        self.assertEqual(self.product_skus(response), ['AKB-GP-AA-2500'])
        self.assertContains(response, 'Нет в наличии')

    def test_empty_product_list_renders_empty_state(self):
        # Если фильтры ничего не нашли, страница должна показать пустое состояние.
        response = self.client.get(reverse('product_list'), {'q': 'нет-такого-товара'})

        self.assertEqual(response.context['products'].count(), 0)
        self.assertContains(response, 'По заданным условиям аккумуляторы не найдены.')

    def test_product_list_sorts_by_name_by_default(self):
        # Без параметра sort используется сортировка по названию.
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.context['selected_sort'], 'name')
        self.assertEqual(self.product_skus(response), self.ordered_skus('name'))

    def test_product_list_sorts_by_required_price_field(self):
        # Проверяем сортировку по обязательному полю price.
        response = self.client.get(reverse('product_list'), {'sort': 'price'})

        self.assertEqual(response.context['selected_sort'], 'price')
        self.assertEqual(self.product_skus(response), self.ordered_skus('price', 'name'))

    def test_product_list_sorts_by_optional_weight_field(self):
        # Проверяем сортировку по необязательному полю weight_grams.
        response = self.client.get(reverse('product_list'), {'sort': 'weight'})

        self.assertEqual(response.context['selected_sort'], 'weight')
        self.assertEqual(self.product_skus(response), self.ordered_skus('weight_grams', 'name'))

    def test_product_list_sorts_by_type_field(self):
        # Проверяем сортировку по связанному полю типа аккумулятора.
        response = self.client.get(reverse('product_list'), {'sort': 'type'})

        self.assertEqual(response.context['selected_sort'], 'type')
        self.assertEqual(self.product_skus(response), self.ordered_skus('battery_type__name', 'name'))

    def test_unknown_sort_falls_back_to_name(self):
        # Неверное значение sort должно заменяться сортировкой по умолчанию.
        response = self.client.get(reverse('product_list'), {'sort': 'wrong'})

        self.assertEqual(response.context['selected_sort'], 'name')
        self.assertEqual(self.product_skus(response), self.ordered_skus('name'))

    def test_filters_and_sort_can_be_combined(self):
        # Фильтрация и сортировка должны работать вместе в одном GET-запросе.
        response = self.client.get(
            reverse('product_list'),
            {'availability': 'in_stock', 'sort': 'price'},
        )

        self.assertEqual(
            self.product_skus(response),
            ['AKB-XIAOMI-20000', 'AKB-CSB-HRL1234', 'AKB-VARTA-D24'],
        )

    def test_product_detail_uses_expected_template_and_context(self):
        # Карточка товара должна использовать свой шаблон и получать нужный product.
        product = Battery.objects.get(sku='AKB-VARTA-D24')

        response = self.client.get(reverse('product_detail', args=[product.pk]))

        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertEqual(response.context['product'], product)
        self.assertContains(response, product.description)
        self.assertContains(response, '540 А')

    def test_about_uses_expected_template_and_text(self):
        # Страница About должна использовать свой шаблон и содержать ожидаемый текст.
        response = self.client.get(reverse('about'))

        self.assertTemplateUsed(response, 'catalog/about.html')
        self.assertContains(response, 'Магазин специализируется на аккумуляторах')
