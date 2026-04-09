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
        """Успешное создание объекта с полным набором корректных данных"""
        bat = Battery(self.valid_data)
        self.assertEqual(bat.brand, 'Panasonic')
        self.assertEqual(bat.weight, 28)

    def test_valid_battery_without_optional_field(self):
        """Успешное создание объекта без необязательного поля"""
        data = self.valid_data.copy()
        del data['weight']
        bat = Battery(data)
        self.assertIsNone(bat.weight)

    def test_calculated_property(self):
        """Проверка вычисляемого свойства"""
        bat = Battery(self.valid_data)
        # 2500 mAh * 1.2 V / 1000 = 3.0 Wh
        self.assertEqual(bat.energy_wh, 3.0)

    # === НЕГАТИВНЫЕ ТЕСТЫ (Проверка обработки ошибок) ===

    def test_not_a_dict(self):
        """Передача не словаря при инициализации"""
        with self.assertRaises(TypeError):
            Battery("просто строка вместо словаря")

    def test_missing_required_field(self):
        """Отсутствие обязательного поля"""
        data = self.valid_data.copy()
        del data['capacity']
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_string(self):
        """Неверный тип для строки"""
        data = self.valid_data.copy()
        data['brand'] = 12345
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_type_boolean(self):
        """Неверный тип для логического поля"""
        data = self.valid_data.copy()
        data['fast_charging'] = "Да"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_type_number_capacity(self):
        """Неверный тип для числа"""
        data = self.valid_data.copy()
        data['capacity'] = "Три тысячи"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_negative_capacity(self):
        """Отрицательная ёмкость"""
        data = self.valid_data.copy()
        data['capacity'] = -500
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_voltage(self):
        """Неверный тип для напряжения"""
        data = self.valid_data.copy()
        data['voltage'] = "двенадцать вольт"
        with self.assertRaises(TypeError):
            Battery(data)

    def test_wrong_choice_enum(self):
        """Значение, не входящее в список допустимых"""
        data = self.valid_data.copy()
        data['form_factor'] = 'Квадратная'
        with self.assertRaises(ValueError):
            Battery(data)

    def test_wrong_type_weight(self):
        """Неверный тип для необязательного поля веса"""
        data = self.valid_data.copy()
        data['weight'] = "очень тяжелый"
        with self.assertRaises(TypeError):
            Battery(data)

if __name__ == '__main__':
    unittest.main()