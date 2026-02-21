import unittest
from battery import Battery

class TestBattery(unittest.TestCase):

    def setUp(self):
        # Эталонный правильный словарь
        self.valid_data = {
            'brand': 'Panasonic',
            'fast_charging': False,
            'capacity': 2500,
            'voltage': 1.2,
            'weight': 28,
            'form_factor': 'AA'
        }

    def test_valid_battery_creation(self):
        """Тест: успешное создание объекта с полным набором корректных данных"""
        bat = Battery(self.valid_data)
        self.assertEqual(bat.brand, 'Panasonic')
        self.assertEqual(bat.weight, 28)

    def test_valid_battery_without_optional_field(self):
        """Тест: успешное создание объекта без необязательного поля 'weight'"""
        data = self.valid_data.copy()
        del data['weight']
        bat = Battery(data)
        self.assertIsNone(bat.weight)

    def test_calculated_property(self):
        """Тест: проверка вычисляемого свойства (Ватт-часы)"""
        # 2500 mAh * 1.2 V / 1000 = 3.0 Wh
        bat = Battery(self.valid_data)
        self.assertEqual(bat.energy_wh, 3.0)

    def test_missing_required_field(self):
        """Тест: выброс исключения при отсутствии обязательного поля"""
        data = self.valid_data.copy()
        del data['capacity']
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_string(self):
        """Тест: неверный тип для строки (brand)"""
        data = self.valid_data.copy()
        data['brand'] = 12345
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_type_boolean(self):
        """Тест: неверный тип для логического поля (fast_charging)"""
        data = self.valid_data.copy()
        data['fast_charging'] = "Да"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_choice_enum(self):
        """Тест: значение, не входящее в список допустимых (form_factor)"""
        data = self.valid_data.copy()
        data['form_factor'] = 'Квадратная'
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_number(self):
        """Тест: неверный тип для числа (capacity)"""
        data = self.valid_data.copy()
        data['capacity'] = "Три тысячи"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_not_a_dict(self):
        """Тест: передача не словаря при инициализации"""
        with self.assertRaises(TypeError):
            Battery("просто строка вместо словаря")

    def test_negative_capacity(self):
        """Тест: отрицательная ёмкость"""
        data = self.valid_data.copy()
        data['capacity'] = -500
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_voltage(self):
        """Тест: неверный тип для напряжения (voltage)"""
        data = self.valid_data.copy()
        data['voltage'] = "двенадцать вольт"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_type_weight(self):
        """Тест: неверный тип для веса (weight)"""
        data = self.valid_data.copy()
        data['weight'] = "очень тяжелый"
        with self.assertRaises(TypeError):
            Battery(data)

if __name__ == '__main__':
    unittest.main()