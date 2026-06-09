from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Battery, Shipment, ShipmentItem
from catalog.tests.helpers import (
    PASSWORD,
    battery_form_data,
    create_battery,
    create_battery_type,
    create_product_specialist,
    create_sales_manager,
    create_user,
)


# Тесты прав доступа проверяют разграничение возможностей гостей, менеджеров и товароведов.
class RoleAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем товар и пользователей с разными ролями для проверки доступа.
        cls.battery_type = create_battery_type()
        cls.product = create_battery(cls.battery_type, sku='AKB-ROLE-001')
        cls.specialist = create_product_specialist()
        cls.manager = create_sales_manager()
        cls.admin = create_user('admin', is_superuser=True)

    def test_guest_can_only_view_catalog_pages(self):
        # Проверяет, что гость видит каталог, но не попадает в закрытые разделы.
        list_response = self.client.get(reverse('product_list'))
        detail_response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        create_response = self.client.get(reverse('product_create'))
        shipment_response = self.client.get(reverse('shipment_list'))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(create_response.status_code, 302)
        self.assertIn('/accounts/login/', create_response.url)
        self.assertEqual(shipment_response.status_code, 302)
        self.assertIn('/accounts/login/', shipment_response.url)

    def test_sales_manager_cannot_manage_catalog_products(self):
        # Проверяет, что менеджер продаж не может создавать, редактировать и удалять товары.
        self.client.login(username=self.manager.username, password=PASSWORD)

        create_response = self.client.get(reverse('product_create'))
        update_response = self.client.get(reverse('product_update', args=[self.product.pk]))
        delete_response = self.client.get(reverse('product_delete', args=[self.product.pk]))

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_product_specialist_can_create_product(self):
        # Проверяет, что товаровед может добавить новый товар через форму.
        self.client.login(username=self.specialist.username, password=PASSWORD)

        response = self.client.post(
            reverse('product_create'),
            battery_form_data(self.battery_type, sku='AKB-CREATE-001'),
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Battery.objects.filter(sku='AKB-CREATE-001').exists())

    def test_product_specialist_can_update_product_description_and_prices(self):
        # Проверяет, что товаровед может изменить описание и цены существующего товара.
        self.client.login(username=self.specialist.username, password=PASSWORD)

        response = self.client.post(
            reverse('product_update', args=[self.product.pk]),
            battery_form_data(
                self.battery_type,
                sku=self.product.sku,
                description='Обновленное описание товароведа.',
                price='6400.00',
                small_wholesale_price='6100.00',
                large_wholesale_price='5800.00',
            ),
        )

        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, 'Обновленное описание товароведа.')
        self.assertEqual(self.product.price, Decimal('6400.00'))

    def test_product_specialist_can_delete_product(self):
        # Проверяет, что товаровед может удалить товар из каталога.
        product = create_battery(self.battery_type, sku='AKB-DELETE-001')
        self.client.login(username=self.specialist.username, password=PASSWORD)

        response = self.client.post(reverse('product_delete', args=[product.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Battery.objects.filter(pk=product.pk).exists())

    def test_admin_can_manage_products(self):
        # Проверяет, что администратор имеет доступ к управлению товарами.
        self.client.login(username=self.admin.username, password=PASSWORD)

        response = self.client.get(reverse('product_update', args=[self.product.pk]))

        self.assertEqual(response.status_code, 200)


# Тесты партий проверяют права менеджеров и расчет стоимости оптовой отправки.
class ShipmentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем товар, двух менеджеров и администратора для сценариев с партиями.
        cls.battery_type = create_battery_type()
        cls.product = create_battery(cls.battery_type, sku='AKB-SHIP-001')
        cls.manager = create_sales_manager('manager-one')
        cls.other_manager = create_sales_manager('manager-two')
        cls.admin = create_user('admin', is_superuser=True)

    def test_sales_manager_can_create_own_shipment(self):
        # Проверяет, что менеджер создает партию, владельцем которой становится он сам.
        self.client.login(username=self.manager.username, password=PASSWORD)

        response = self.client.post(reverse('shipment_create'))

        self.assertEqual(response.status_code, 302)
        shipment = Shipment.objects.get()
        self.assertEqual(shipment.owner, self.manager)

    def test_sales_manager_can_add_product_to_own_shipment(self):
        # Проверяет добавление товара в свою партию и выбор цены по количеству.
        shipment = Shipment.objects.create(owner=self.manager)
        self.client.login(username=self.manager.username, password=PASSWORD)

        response = self.client.post(
            reverse('shipment_add_item', args=[shipment.pk]),
            {'product': self.product.pk, 'quantity': 5},
        )

        self.assertEqual(response.status_code, 302)
        item = ShipmentItem.objects.get(shipment=shipment)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.unit_price, Decimal('6200.00'))

    def test_manager_sees_only_own_shipments(self):
        # Проверяет, что менеджер в списке видит только свои партии.
        own_shipment = Shipment.objects.create(owner=self.manager, title='Своя партия')
        Shipment.objects.create(owner=self.other_manager, title='Чужая партия')
        self.client.login(username=self.manager.username, password=PASSWORD)

        response = self.client.get(reverse('shipment_list'))

        self.assertContains(response, own_shipment.title)
        self.assertNotContains(response, 'Чужая партия')

    def test_one_manager_cannot_change_another_manager_shipment(self):
        # Проверяет запрет доступа менеджера к чужой партии и ее позициям.
        shipment = Shipment.objects.create(owner=self.manager)
        item = ShipmentItem.objects.create(shipment=shipment, product=self.product, quantity=3)
        self.client.login(username=self.other_manager.username, password=PASSWORD)

        detail_response = self.client.get(reverse('shipment_detail', args=[shipment.pk]))
        add_response = self.client.post(
            reverse('shipment_add_item', args=[shipment.pk]),
            {'product': self.product.pk, 'quantity': 2},
        )
        delete_response = self.client.post(
            reverse('shipment_delete_item', args=[shipment.pk, item.pk]),
        )

        self.assertEqual(detail_response.status_code, 403)
        self.assertEqual(add_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(shipment.items.count(), 1)

    def test_admin_can_open_any_manager_shipment(self):
        # Проверяет, что администратор может открыть партию любого менеджера.
        shipment = Shipment.objects.create(owner=self.manager)
        self.client.login(username=self.admin.username, password=PASSWORD)

        response = self.client.get(reverse('shipment_detail', args=[shipment.pk]))

        self.assertEqual(response.status_code, 200)

    def test_shipment_total_uses_wholesale_prices_and_additional_discount(self):
        # Проверяет расчет партии: разные оптовые цены и дополнительная скидка.
        shipment = Shipment.objects.create(
            owner=self.manager,
            additional_discount_percent=Decimal('10.00'),
        )
        ShipmentItem.objects.create(shipment=shipment, product=self.product, quantity=3)
        ShipmentItem.objects.create(shipment=shipment, product=self.product, quantity=5)
        ShipmentItem.objects.create(shipment=shipment, product=self.product, quantity=20)

        self.assertEqual(shipment.subtotal, Decimal('168500.00'))
        self.assertEqual(shipment.discount_amount, Decimal('16850.00'))
        self.assertEqual(shipment.total, Decimal('151650.00'))

    def test_sales_manager_can_update_additional_discount(self):
        # Проверяет, что менеджер может изменить название партии и дополнительную скидку.
        shipment = Shipment.objects.create(owner=self.manager)
        self.client.login(username=self.manager.username, password=PASSWORD)

        response = self.client.post(
            reverse('shipment_detail', args=[shipment.pk]),
            {'title': 'Партия для клиента', 'additional_discount_percent': '7.50'},
        )

        self.assertEqual(response.status_code, 302)
        shipment.refresh_from_db()
        self.assertEqual(shipment.title, 'Партия для клиента')
        self.assertEqual(shipment.additional_discount_percent, Decimal('7.50'))
