from django.test import TestCase
from django.urls import reverse

class CatalogRoutesTest(TestCase):
    def test_product_list_route(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_route(self):
        # Проверяем, что страница аккумулятора с id=1 загружается успешно (код 200)
        response = self.client.get(reverse('product_detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)