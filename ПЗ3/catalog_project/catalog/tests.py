import os
from unittest import SkipTest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse

try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.common.by import By
except ImportError:
    webdriver = None
    WebDriverException = Exception
    By = None


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


class CatalogSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = None

        if webdriver is None:
            cls._skip_after_server_start(
                'Selenium не установлен. Установите зависимости командой: '
                'python3 -m pip install -r requirements.txt'
            )

        try:
            cls.browser = cls._create_webdriver()
        except WebDriverException as exc:
            cls._skip_after_server_start(
                f'Не удалось запустить браузер через Selenium: {exc}'
            )

        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        if getattr(cls, 'browser', None):
            cls.browser.quit()
        super().tearDownClass()

    @classmethod
    def _skip_after_server_start(cls, reason):
        super(CatalogSeleniumTests, cls).tearDownClass()
        raise SkipTest(reason)

    @staticmethod
    def _create_webdriver():
        browser_name = os.environ.get('SELENIUM_BROWSER', 'chrome').lower()

        if browser_name == 'safari':
            return webdriver.Safari()
        if browser_name == 'chrome':
            return webdriver.Chrome()
        if browser_name == 'firefox':
            return webdriver.Firefox()
        if browser_name == 'edge':
            return webdriver.Edge()

        raise WebDriverException(
            f'Неподдерживаемый браузер "{browser_name}". '
            'Используйте safari, chrome, firefox или edge.'
        )

    def test_user_can_open_catalog_and_navigate_site(self):
        self.browser.get(f'{self.live_server_url}{reverse("product_list")}')

        self.assertEqual(self.browser.title, 'Каталог аккумуляторов')
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h1').text,
            'Магазин аккумуляторов'
        )

        self.browser.find_element(By.LINK_TEXT, 'О магазине').click()
        self.assertEqual(self.browser.title, 'О магазине аккумуляторов')
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h1').text,
            'О нашем магазине'
        )

        self.browser.find_element(By.LINK_TEXT, 'Назад к списку аккумуляторов').click()
        self.browser.find_element(By.LINK_TEXT, 'Автомобильный аккумулятор VARTA').click()

        self.assertEqual(self.browser.title, 'Информация об аккумуляторе')
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h1').text,
            'Автомобильный аккумулятор VARTA'
        )
        self.assertIn(
            'Емкость 60 Ач',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
