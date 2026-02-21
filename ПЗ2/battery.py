class Battery:
    ALLOWED_FORM_FACTORS = ('AA', 'AAA', '18650', '21700', 'PowerBank', 'другое')

    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть переданы в виде словаря.")

        # Проверка обязательных полей
        required_keys = {'brand', 'fast_charging', 'capacity', 'voltage', 'form_factor'}
        missing_keys = required_keys - set(data.keys())
        if missing_keys:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing_keys)}")

        # 1. Строка: brand
        if not isinstance(data['brand'], str):
            raise TypeError("Поле 'brand' должно быть строкой.")
        self.brand = data['brand']

        # 2. Логический тип: fast_charging
        # Используем type() is bool, т.к. isinstance(True, int) вернет True в Python
        if type(data['fast_charging']) is not bool:
            raise TypeError("Поле 'fast_charging' должно быть логическим типом (True/False).")
        self.fast_charging = data['fast_charging']

        # 3. Число: capacity и voltage
        if not isinstance(data['capacity'], (int, float)):
            raise TypeError("Поле 'capacity' должно быть числом.")
        if data['capacity'] <= 0:
            raise ValueError("Ёмкость должна быть больше нуля.")
        self.capacity = data['capacity']

        if not isinstance(data['voltage'], (int, float)):
            raise TypeError("Поле 'voltage' должно быть числом.")
        self.voltage = data['voltage']

        # 4. Выбор из вариантов: form_factor
        if data['form_factor'] not in self.ALLOWED_FORM_FACTORS:
            raise ValueError(f"Поле 'form_factor' должно быть одним из: {self.ALLOWED_FORM_FACTORS}")
        self.form_factor = data['form_factor']

        # 5. Необязательное поле: weight (число)
        self.weight = None
        if 'weight' in data:
            if not isinstance(data['weight'], (int, float)):
                raise TypeError("Поле 'weight' должно быть числом.")
            self.weight = data['weight']

    @property
    def energy_wh(self) -> float:
        """Вычисляемое свойство: Энергия в ватт-часах (Вт·ч)"""
        # Формула: (мАч * В) / 1000
        return round((self.capacity * self.voltage) / 1000, 2)