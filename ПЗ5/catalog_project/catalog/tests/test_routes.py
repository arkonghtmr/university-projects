from django.test import TestCase
from django.urls import resolve, reverse

from catalog import views
from catalog.models import Battery, BatteryType


class CatalogRouteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем один товар, чтобы проверять маршрут карточки существующего товара.
        battery_type = BatteryType.objects.create(name='Автомобильный', slug='car')
        cls.product = Battery.objects.create(
            sku='AKB-VARTA-D24',
            name='VARTA Blue Dynamic D24',
            brand='VARTA',
            battery_type=battery_type,
            capacity_mah=60000,
            voltage_v='12.00',
            starting_current_a=540,
            weight_grams=14500,
            price='6500.00',
            stock_quantity=4,
            warranty_months=24,
            description='Автомобильный аккумулятор емкостью 60 Ач с пусковым током 540 А.',
        )

    def test_product_list_url_resolves_to_product_list_view(self):
        # Проверяем, что имя маршрута product_list связано с view списка товаров.
        match = resolve(reverse('product_list'))

        self.assertEqual(match.func, views.product_list)

    def test_product_detail_url_resolves_to_product_detail_view(self):
        # Проверяем, что URL карточки товара ведет к view product_detail.
        match = resolve(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(match.func, views.product_detail)

    def test_about_url_resolves_to_about_view(self):
        # Проверяем, что URL страницы About ведет к view about.
        match = resolve(reverse('about'))

        self.assertEqual(match.func, views.about)

    def test_product_list_reverse_returns_catalog_root(self):
        # Главная страница каталога должна находиться в корне сайта.
        self.assertEqual(reverse('product_list'), '/')

    def test_product_list_get_returns_200(self):
        # GET-запрос к списку товаров должен успешно открывать страницу.
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_get_returns_200(self):
        # Карточка существующего товара должна открываться без ошибки.
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_missing_product_returns_404(self):
        # Если товара нет в базе, карточка должна возвращать 404.
        response = self.client.get(reverse('product_detail', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_about_get_returns_200(self):
        # Статическая страница About должна быть доступна.
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
