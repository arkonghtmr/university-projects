class Battery:
    ALLOWED_FORM_FACTORS = ('AA', 'AAA', '18650', '21700', 'PowerBank', 'другое')

    def __init__(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть переданы в виде словаря.")

        required_keys = {'brand', 'fast_charging', 'capacity', 'voltage', 'form_factor'}
        missing_keys = required_keys - set(data.keys())
        if missing_keys:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing_keys)}")

        if not isinstance(data['brand'], str):
            raise TypeError("Поле 'brand' должно быть строкой.")
        self.brand = data['brand']

        if type(data['fast_charging']) is not bool:
            raise TypeError("Поле 'fast_charging' должно быть логическим типом (True/False).")
        self.fast_charging = data['fast_charging']

        if not isinstance(data['capacity'], (int, float)):
            raise TypeError("Поле 'capacity' должно быть числом.")
        if data['capacity'] <= 0:
            raise ValueError("Ёмкость должна быть больше нуля.")
        self.capacity = data['capacity']

        if not isinstance(data['voltage'], (int, float)):
            raise TypeError("Поле 'voltage' должно быть числом.")
        self.voltage = data['voltage']

        if data['form_factor'] not in self.ALLOWED_FORM_FACTORS:
            raise ValueError(f"Поле 'form_factor' должно быть одним из: {self.ALLOWED_FORM_FACTORS}")
        self.form_factor = data['form_factor']

        self.weight = None
        if 'weight' in data:
            if not isinstance(data['weight'], (int, float)):
                raise TypeError("Поле 'weight' должно быть числом.")
            self.weight = data['weight']

    @property
    def energy_wh(self) -> float:
        return round((self.capacity * self.voltage) / 1000, 2)