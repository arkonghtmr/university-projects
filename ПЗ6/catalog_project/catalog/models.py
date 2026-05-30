from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse


class BatteryType(models.Model):
    name = models.CharField('Название типа', max_length=80, unique=True)
    slug = models.SlugField('Код для фильтра', max_length=90, unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип аккумулятора'
        verbose_name_plural = 'Типы аккумуляторов'

    def __str__(self):
        return self.name


class BatteryQuerySet(models.QuerySet):
    def by_type(self, battery_type):
        if isinstance(battery_type, BatteryType):
            return self.filter(battery_type=battery_type)
        return self.filter(battery_type__slug=battery_type)

    def in_stock(self):
        return self.filter(stock_quantity__gt=0)

    def high_capacity(self):
        return self.filter(capacity_mah__gte=20000)

    def heavy(self):
        return self.filter(weight_grams__gte=5000)


class Battery(models.Model):
    sku = models.CharField(
        'Артикул',
        max_length=32,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9-]+$',
                message='Артикул должен состоять из латинских заглавных букв, цифр и дефисов.',
            )
        ],
    )
    name = models.CharField('Название', max_length=120)
    brand = models.CharField('Бренд', max_length=80)
    battery_type = models.ForeignKey(
        BatteryType,
        on_delete=models.PROTECT,
        related_name='batteries',
        verbose_name='Тип аккумулятора',
    )
    capacity_mah = models.PositiveIntegerField(
        'Емкость, мАч',
        validators=[MinValueValidator(1), MaxValueValidator(500000)],
    )
    voltage_v = models.DecimalField(
        'Напряжение, В',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
    )
    starting_current_a = models.PositiveIntegerField(
        'Пусковой ток, А',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3000)],
    )
    weight_grams = models.PositiveIntegerField(
        'Вес, г',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100000)],
    )
    price = models.DecimalField(
        'Цена за единицу, руб.',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    small_wholesale_price = models.DecimalField(
        'Цена мелкого опта, руб.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    small_wholesale_min_quantity = models.PositiveIntegerField(
        'Количество для мелкого опта',
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100000)],
    )
    large_wholesale_price = models.DecimalField(
        'Цена крупного опта, руб.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    large_wholesale_min_quantity = models.PositiveIntegerField(
        'Количество для крупного опта',
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(100000)],
    )
    stock_quantity = models.PositiveIntegerField(
        'Остаток на складе',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
    )
    warranty_months = models.PositiveSmallIntegerField(
        'Гарантия, мес.',
        default=12,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
    )
    fast_charge = models.BooleanField('Поддержка быстрой зарядки', default=False)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    objects = BatteryQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Аккумулятор'
        verbose_name_plural = 'Аккумуляторы'
        constraints = [
            models.CheckConstraint(condition=Q(price__gt=0), name='battery_price_positive'),
            models.CheckConstraint(condition=Q(capacity_mah__gt=0), name='battery_capacity_positive'),
            models.CheckConstraint(condition=Q(voltage_v__gt=0), name='battery_voltage_positive'),
            models.CheckConstraint(condition=Q(stock_quantity__gte=0), name='battery_stock_non_negative'),
            models.CheckConstraint(
                condition=Q(weight_grams__isnull=True) | Q(weight_grams__gt=0),
                name='battery_weight_null_or_positive',
            ),
            models.CheckConstraint(
                condition=Q(starting_current_a__isnull=True) | Q(starting_current_a__gt=0),
                name='battery_starting_current_null_or_positive',
            ),
            models.CheckConstraint(
                condition=Q(warranty_months__gte=0) & Q(warranty_months__lte=120),
                name='battery_warranty_valid_range',
            ),
        ]

    @property
    def is_heavy(self):
        return self.weight_grams is not None and self.weight_grams >= 5000

    @property
    def is_high_capacity(self):
        return self.capacity_mah >= 20000

    def get_price_for_quantity(self, quantity):
        if self.large_wholesale_price and quantity >= self.large_wholesale_min_quantity:
            return self.large_wholesale_price
        if self.small_wholesale_price and quantity >= self.small_wholesale_min_quantity:
            return self.small_wholesale_price
        return self.price

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])

    def __str__(self):
        return f'{self.brand} {self.name} ({self.sku})'


class Shipment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name='Менеджер',
    )
    title = models.CharField('Название партии', max_length=120, default='Партия на отправку')
    additional_discount_percent = models.DecimalField(
        'Дополнительная скидка, %',
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'Партия на отправку'
        verbose_name_plural = 'Партии на отправку'

    @property
    def subtotal(self):
        return sum((item.total_price for item in self.items.select_related('product')), Decimal('0.00'))

    @property
    def discount_amount(self):
        return (self.subtotal * self.additional_discount_percent / Decimal('100')).quantize(Decimal('0.01'))

    @property
    def total(self):
        return self.subtotal - self.discount_amount

    def can_be_changed_by(self, user):
        return user.is_superuser or self.owner_id == user.id

    def __str__(self):
        return f'{self.title} ({self.owner})'


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Партия',
    )
    product = models.ForeignKey(
        Battery,
        on_delete=models.PROTECT,
        related_name='shipment_items',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1), MaxValueValidator(100000)],
    )

    class Meta:
        verbose_name = 'Позиция партии'
        verbose_name_plural = 'Позиции партии'

    @property
    def unit_price(self):
        return self.product.get_price_for_quantity(self.quantity)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f'{self.product} x {self.quantity}'
