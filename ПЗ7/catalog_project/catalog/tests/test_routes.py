from django.test import TestCase
from django.urls import resolve, reverse

from catalog import views
from catalog.models import Battery, BatteryType, Shipment, ShipmentItem
from catalog.tests.helpers import create_sales_manager


# Тесты маршрутов проверяют привязку URL к вьюхам и базовые HTTP-ответы.
class CatalogRouteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Товар, менеджер и партия нужны для URL, где используются pk объектов.
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
        cls.manager = create_sales_manager()
        cls.shipment = Shipment.objects.create(owner=cls.manager)
        cls.shipment_item = ShipmentItem.objects.create(
            shipment=cls.shipment,
            product=cls.product,
            quantity=2,
        )

    def test_product_list_url_resolves_to_product_list_view(self):
        # Проверяет, что корневой URL каталога ведет во вьюху списка товаров.
        match = resolve(reverse('product_list'))

        self.assertEqual(match.func, views.product_list)

    def test_product_detail_url_resolves_to_product_detail_view(self):
        # Проверяет, что URL карточки товара ведет во вьюху детальной страницы.
        match = resolve(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(match.func, views.product_detail)

    def test_product_create_url_resolves_to_product_create_view(self):
        # Проверяет, что URL создания товара связан с правильной вьюхой.
        match = resolve(reverse('product_create'))

        self.assertEqual(match.func, views.product_create)

    def test_product_update_url_resolves_to_product_update_view(self):
        # Проверяет, что URL редактирования товара связан с правильной вьюхой.
        match = resolve(reverse('product_update', args=[self.product.pk]))

        self.assertEqual(match.func, views.product_update)

    def test_product_delete_url_resolves_to_product_delete_view(self):
        # Проверяет, что URL удаления товара связан с правильной вьюхой.
        match = resolve(reverse('product_delete', args=[self.product.pk]))

        self.assertEqual(match.func, views.product_delete)

    def test_shipment_routes_resolve_to_expected_views(self):
        # Проверяет URL партий: список, создание, детали, добавление и удаление позиции.
        self.assertEqual(resolve(reverse('shipment_list')).func, views.shipment_list)
        self.assertEqual(resolve(reverse('shipment_create')).func, views.shipment_create)
        self.assertEqual(resolve(reverse('shipment_detail', args=[self.shipment.pk])).func, views.shipment_detail)
        self.assertEqual(resolve(reverse('shipment_add_item', args=[self.shipment.pk])).func, views.shipment_add_item)
        self.assertEqual(
            resolve(reverse('shipment_delete_item', args=[self.shipment.pk, self.shipment_item.pk])).func,
            views.shipment_delete_item,
        )

    def test_about_url_resolves_to_about_view(self):
        # Проверяет, что URL страницы о магазине связан с нужной вьюхой.
        match = resolve(reverse('about'))

        self.assertEqual(match.func, views.about)

    def test_product_list_reverse_returns_catalog_root(self):
        # Проверяет, что имя маршрута product_list строит корневой путь каталога.
        self.assertEqual(reverse('product_list'), '/')

    def test_product_list_get_returns_200(self):
        # Проверяет, что главная страница каталога доступна пользователю.
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_get_returns_200(self):
        # Проверяет, что карточка существующего товара открывается без ошибки.
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_missing_product_returns_404(self):
        # Проверяет, что несуществующий товар возвращает HTTP 404.
        response = self.client.get(reverse('product_detail', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_about_get_returns_200(self):
        # Проверяет, что страница о магазине открывается без ошибки.
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
