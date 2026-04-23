import unittest
from battery import Battery

class TestBattery(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            'brand': 'Panasonic',
            'fast_charging': False,
            'capacity': 2500,
            'voltage': 1.2,
            'weight': 28,
            'form_factor': 'AA'
        }

    # === ПОЗИТИВНЫЕ ТЕСТЫ ===

    def test_valid_battery_creation(self):
        bat = Battery(self.valid_data)
        self.assertEqual(bat.brand, 'Panasonic')
        self.assertEqual(bat.weight, 28)

    def test_valid_battery_without_optional_field(self):
        del self.valid_data['weight']
        bat = Battery(self.valid_data)
        self.assertIsNone(bat.weight)

    def test_calculated_property(self):
        bat = Battery(self.valid_data)
        # 2500 mAh * 1.2 V / 1000 = 3.0 Wh
        self.assertEqual(bat.energy_wh, 3.0)

    # === НЕГАТИВНЫЕ ТЕСТЫ ===

    def test_not_a_dict(self):
        with self.assertRaises(TypeError):
            Battery("просто строка вместо словаря")

    def test_missing_required_field(self):
        del self.valid_data['capacity']
        with self.assertRaises(ValueError):
            Battery(self.valid_data)

    def test_wrong_type_string(self):
        self.valid_data['brand'] = 12345
        with self.assertRaises(TypeError):
            Battery(self.valid_data)

    def test_wrong_type_boolean(self):
        self.valid_data['fast_charging'] = "Да"
        with self.assertRaises(TypeError):
            Battery(self.valid_data)

    def test_wrong_type_number_capacity(self):
        self.valid_data['capacity'] = "Три тысячи"
        with self.assertRaises(TypeError):
            Battery(self.valid_data)

    def test_negative_capacity(self):
        self.valid_data['capacity'] = -500
        with self.assertRaises(ValueError):
            Battery(self.valid_data)

    def test_wrong_type_voltage(self):
        self.valid_data['voltage'] = "двенадцать вольт"
        with self.assertRaises(TypeError):
            Battery(self.valid_data)

    def test_wrong_choice_enum(self):
        self.valid_data['form_factor'] = 'Квадратная'
        with self.assertRaises(ValueError):
            Battery(self.valid_data)

    def test_wrong_type_weight(self):
        self.valid_data['weight'] = "очень тяжелый"
        with self.assertRaises(TypeError):
            Battery(self.valid_data)

if __name__ == '__main__':
    unittest.main()