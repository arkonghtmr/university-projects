# Test Plan Identifier

TP-AKB-2026-05

# Introduction

Тест-план описывает проверку модуля отображения каталога аккумуляторов в практической работе 5. Проверяются GET-страницы каталога, карточки товара и About, а также контекст, шаблоны, фильтрация и сортировка списка товаров.

# Test Items

Проверяемые view-функции:

- `product_list`
- `product_detail`
- `about`

Проверяемые тестовые файлы:

- `catalog/tests/test_routes.py`
- `catalog/tests/test_content.py`

# Features to be tested

- доступность URL и связь URL с нужной view-функцией;
- статус-коды GET-запросов `200` и `404`;
- загрузка ожидаемых шаблонов;
- наличие ключей `products`, `battery_types`, `product` в контексте;
- вывод товаров, созданных в `setUpTestData`;
- поиск по строке запроса;
- фильтрация группы товаров по типу аккумулятора;
- сортировка по названию;
- сортировка по обязательному полю `price`;
- сортировка по необязательному полю `weight_grams`;
- сортировка по типу `battery_type`;
- статическая страница About;
- корректное сообщение для пустого списка.

# Features NOT to be tested

- авторизация и права доступа;
- формы создания и редактирования;
- POST-запросы и изменение данных;
- API;
- админка Django;
- бизнес-правила моделей из предыдущей практической работы.

# Approach

Тестирование выполняется через `django.test.TestCase` и `django.test.Client`. Данные создаются в `setUpTestData`, запросы выполняются только методом GET, URL строятся через `reverse()`, соответствие URL и view проверяется через `resolve()`.

# Item Pass/Fail Criteria

Тест считается пройденным, если получен ожидаемый статус-код, загружен правильный шаблон, контекст содержит нужные ключи и данные, а порядок и состав товаров совпадают с ожидаемым сценарием. Тест считается проваленным при ошибке маршрутизации, неверном статус-коде, отсутствии данных в контексте, неправильной фильтрации или сортировке.

# Suspension Criteria

Тестирование приостанавливается, если падает более 30% тестов, не создается тестовая база данных, не применяются миграции или фикстура каталога не загружается.

# Test Deliverables

- код тестов в пакете `catalog/tests`;
- результат запуска `python manage.py test catalog.tests --verbosity=2`;
- отчет покрытия `coverage run --source='.' manage.py test catalog.tests` и `coverage report`;
- этот файл `TEST_PLAN.md`.

# Test Case Matrix

| ID | Сценарий | URL | Метод | Ожидаемый результат | Приоритет |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Главная страница каталога | `/` | GET | Status 200, view `product_list` | High |
| TC-02 | Список содержит товары | `/` | GET | Status 200, context `products` не пуст | High |
| TC-03 | Контекст списка | `/` | GET | Context содержит `products`, `battery_types` | High |
| TC-04 | Поиск по товару | `/?q=VARTA` | GET | В списке только товар VARTA | High |
| TC-05 | Фильтрация по типу | `/?type=aa-aaa` | GET | В списке только товары типа AA/AAA | High |
| TC-06 | Сортировка по названию | `/` | GET | Товары отсортированы по `name` | High |
| TC-07 | Сортировка по обязательному полю | `/?sort=price` | GET | Товары отсортированы по `price` | High |
| TC-08 | Сортировка по необязательному полю | `/?sort=weight` | GET | Товары отсортированы по `weight_grams` | High |
| TC-09 | Сортировка по типу | `/?sort=type` | GET | Товары отсортированы по `battery_type__name` | High |
| TC-10 | Неверная сортировка | `/?sort=wrong` | GET | Используется сортировка по `name` | Medium |
| TC-11 | Детальная страница | `/product/<pk>/` | GET | Status 200, шаблон `product_detail.html`, context `product` | High |
| TC-12 | Несуществующий товар | `/product/999/` | GET | Status 404 | High |
| TC-13 | Страница About | `/about/` | GET | Status 200, шаблон `about.html`, есть текст о магазине | Medium |
| TC-14 | Пустой список | `/?q=нет-такого-товара` | GET | Status 200, показано сообщение о пустом результате | Medium |

# Verification Report

Команда:

```bash
python manage.py test catalog.tests --verbosity=2
```

В текущем окружении выполнен эквивалент:

```bash
python3 manage.py test catalog.tests --verbosity=2
```

Результат:

```text
Found 23 test(s).
Ran 23 tests in 0.045s
OK
```

Команды покрытия:

```bash
coverage run --source='.' manage.py test catalog.tests
coverage report
```

Результат покрытия:

```text
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
catalog/views.py                        29      0   100%
catalog/tests/test_content.py           83      0   100%
catalog/tests/test_routes.py            32      0   100%
TOTAL                                  279     17    94%
```
