from django.test import TestCase
from django.urls import resolve, reverse

from catalog import views
from catalog.models import Battery, BatteryType


class CatalogRouteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        match = resolve(reverse('product_list'))

        self.assertEqual(match.func, views.product_list)

    def test_product_detail_url_resolves_to_product_detail_view(self):
        match = resolve(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(match.func, views.product_detail)

    def test_about_url_resolves_to_about_view(self):
        match = resolve(reverse('about'))

        self.assertEqual(match.func, views.about)

    def test_product_list_reverse_returns_catalog_root(self):
        self.assertEqual(reverse('product_list'), '/')

    def test_product_list_get_returns_200(self):
        response = self.client.get(reverse('product_list'))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_get_returns_200(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))

        self.assertEqual(response.status_code, 200)

    def test_product_detail_missing_product_returns_404(self):
        response = self.client.get(reverse('product_detail', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_about_get_returns_200(self):
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
