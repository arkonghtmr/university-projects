from django import forms

from .models import Battery, Shipment, ShipmentItem


class BatteryForm(forms.ModelForm):
    class Meta:
        model = Battery
        fields = (
            'sku',
            'name',
            'brand',
            'battery_type',
            'capacity_mah',
            'voltage_v',
            'starting_current_a',
            'weight_grams',
            'price',
            'small_wholesale_price',
            'small_wholesale_min_quantity',
            'large_wholesale_price',
            'large_wholesale_min_quantity',
            'stock_quantity',
            'warranty_months',
            'fast_charge',
            'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        unit_price = cleaned_data.get('price')
        small_price = cleaned_data.get('small_wholesale_price')
        large_price = cleaned_data.get('large_wholesale_price')
        small_quantity = cleaned_data.get('small_wholesale_min_quantity')
        large_quantity = cleaned_data.get('large_wholesale_min_quantity')

        if unit_price and small_price and small_price > unit_price:
            self.add_error('small_wholesale_price', 'Цена мелкого опта не должна быть выше цены за единицу.')
        if small_price and large_price and large_price > small_price:
            self.add_error('large_wholesale_price', 'Цена крупного опта не должна быть выше цены мелкого опта.')
        if small_quantity and large_quantity and large_quantity <= small_quantity:
            self.add_error('large_wholesale_min_quantity', 'Количество крупного опта должно быть больше мелкого опта.')

        return cleaned_data


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ('title', 'additional_discount_percent')


class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ('product', 'quantity')
