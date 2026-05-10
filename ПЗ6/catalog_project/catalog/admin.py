from django.contrib import admin

from .models import Battery, BatteryType, Shipment, ShipmentItem


@admin.register(BatteryType)
class BatteryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'brand',
        'battery_type',
        'capacity_mah',
        'voltage_v',
        'price',
        'small_wholesale_price',
        'large_wholesale_price',
        'stock_quantity',
        'heavy_marker',
        'high_capacity_marker',
    )
    list_display_links = ('sku', 'name')
    list_editable = ('price', 'small_wholesale_price', 'large_wholesale_price', 'stock_quantity')
    list_filter = ('battery_type', 'brand', 'fast_charge')
    search_fields = ('sku', 'name', 'brand', 'description')
    autocomplete_fields = ('battery_type',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основное', {'fields': ('sku', 'name', 'brand', 'battery_type', 'description')}),
        (
            'Характеристики',
            {
                'fields': (
                    'capacity_mah',
                    'voltage_v',
                    'starting_current_a',
                    'weight_grams',
                    'fast_charge',
                )
            },
        ),
        (
            'Продажи',
            {
                'fields': (
                    'price',
                    'small_wholesale_price',
                    'small_wholesale_min_quantity',
                    'large_wholesale_price',
                    'large_wholesale_min_quantity',
                    'stock_quantity',
                    'warranty_months',
                )
            },
        ),
        ('Служебные поля', {'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(boolean=True, description='Тяжелый')
    def heavy_marker(self, obj):
        return obj.is_heavy

    @admin.display(boolean=True, description='Большая емкость')
    def high_capacity_marker(self, obj):
        return obj.is_high_capacity


class ShipmentItemInline(admin.TabularInline):
    model = ShipmentItem
    extra = 0
    readonly_fields = ('unit_price', 'total_price')


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'additional_discount_percent', 'subtotal', 'discount_amount', 'total')
    list_filter = ('owner',)
    search_fields = ('title', 'owner__username')
    inlines = (ShipmentItemInline,)
