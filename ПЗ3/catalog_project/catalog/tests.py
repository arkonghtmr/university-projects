from django.test import TestCase
from django.urls import reverse

class CatalogURLTests(TestCase):

    def test_product_list_page_is_accessible(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_about_page_is_accessible(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_is_accessible(self):
        url = reverse('product_detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)