# ПЗ7. Проект каталога: контейнеризация и подготовка к запуску

## Что нужно было сделать по методичке

Практическая работа 7 называется "Проект каталог. Подготовка к бою". Ее смысл - показать, что проект каталога работает не только на машине разработчика, но и в воспроизводимом окружении через Docker.

По методичке требовалось:

- сделать Docker-образ Django-проекта;
- использовать WSGI-сервер для запуска Django;
- вынести базу данных из контейнера во внешний Docker volume;
- поднять два контейнера через Docker Compose: nginx и Django;
- настроить nginx как внешний HTTP-прокси к Django-приложению;
- запустить линтер и показать, что код удовлетворяет PEP8 со статусом `ok`;
- запустить тесты в контейнере и показать, что они проходят без ошибок со статусом `ok`;
- приложить Docker-файлы и файл Compose;
- приложить скриншоты успешного запуска линтера и тестов с командами запуска.

## Как вообще работает ПЗ7

Проект `ПЗ7/catalog_project` - это Django-каталог аккумуляторов из предыдущих работ, подготовленный к запуску в контейнерах. Функциональность каталога осталась такой же, как в ПЗ6: есть товары, роли пользователей, формы управления товарами, партии на отправку, оптовые цены и расчет итоговой суммы партии.

ПЗ7 добавляет инфраструктурный слой:

- `Dockerfile` собирает образ Django-приложения;
- `docker-compose.yml` запускает связку `web` + `nginx`;
- `requirements.txt` фиксирует зависимости проекта;
- `scripts/entrypoint.sh` выполняет миграции, сбор статики и загрузку фикстур;
- `nginx/default.conf` проксирует HTTP-запросы в Django-контейнер;
- `setup.cfg` содержит настройки `pycodestyle`;
- `ОТЧЕТ.md` описывает команды запуска и содержит ссылки на скриншоты.

## Как работает Docker-образ

Образ собирается из `python:3.12-slim`. Внутри создается рабочая директория `/app`, устанавливаются зависимости из `requirements.txt`, копируется код проекта и настраивается запуск от отдельного пользователя `django`.

Контейнер Django запускает команду:

```bash
gunicorn catalog_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Это закрывает требование методички про WSGI-сервер: Django в контейнере обслуживается через `gunicorn`, а не через development-сервер `runserver`.

## Как работает Docker Compose

В `docker-compose.yml` описаны два сервиса:

- `web` - контейнер Django-приложения;
- `nginx` - контейнер nginx, который принимает запросы с хоста и проксирует их в `web`.

Сервис `web` получает настройки через переменные окружения:

- `DJANGO_DEBUG=False`;
- `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web`;
- `DJANGO_DB_PATH=/data/db.sqlite3`;
- `DJANGO_STATIC_ROOT=/static`;
- `DJANGO_SECRET_KEY=pz7-local-docker-secret-key`.

База SQLite вынесена из контейнера в volume `catalog_db`, который подключается как `/data`. Поэтому файл `/data/db.sqlite3` сохраняется вне жизненного цикла контейнера. Статика вынесена в volume `static_files`, который доступен Django для `collectstatic` и nginx для отдачи `/static/`.

Сервис `nginx` открывает порт:

```text
http://127.0.0.1:8087/
```

nginx проксирует основной трафик в `web:8000`, а статические файлы отдает из `/static/`.

## Как работает entrypoint

Перед запуском gunicorn выполняется `scripts/entrypoint.sh`:

```sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata battery_catalog
exec "$@"
```

Это значит, что при старте контейнера автоматически применяются миграции, собирается статика и загружаются начальные данные каталога из фикстуры `battery_catalog`.

## Как проверяется качество

По методичке нужно показать две проверки:

- линтер проходит со статусом `ok`;
- тесты проходят в контейнере со статусом `ok`.

Для линтера используется `pycodestyle` с настройками из `setup.cfg`. Для функциональной проверки используются те же 46 Django-тестов, которые проверяют каталог, формы, роли, партии и расчеты.

# Test Plan Identifier

TP-AKB-2026-07

# Introduction

Тест-план описывает проверку практической работы 7 "Проект каталог. Подготовка к бою". Цель проверки - убедиться, что Django-проект корректно контейнеризован, запускается через WSGI-сервер, работает за nginx, хранит данные вне контейнера и проходит линтер и автоматические тесты.

В этой работе тестируется не новая бизнес-логика каталога, а готовность проекта к воспроизводимому запуску в Docker-окружении.

# Test Items

Проверяемые инфраструктурные файлы:

- `Dockerfile`;
- `docker-compose.yml`;
- `requirements.txt`;
- `setup.cfg`;
- `scripts/entrypoint.sh`;
- `nginx/default.conf`.

Проверяемые Django-модули:

- `catalog.models`;
- `catalog.forms`;
- `catalog.views`;
- `catalog.urls`;
- `catalog.tests`.

Проверяемые контейнеры:

- `web` - Django + gunicorn;
- `nginx` - reverse proxy и отдача статики.

Проверяемые Docker volumes:

- `catalog_db` - хранение SQLite-базы `/data/db.sqlite3`;
- `static_files` - хранение собранной статики `/static`.

# Features to be tested

Проверяются следующие возможности:

- Docker-образ Django-приложения собирается без ошибок;
- контейнер `web` запускает Django через `gunicorn`;
- `docker-compose.yml` поднимает два сервиса: `web` и `nginx`;
- nginx проксирует запросы в Django-контейнер;
- приложение доступно с хоста по адресу `http://127.0.0.1:8087/`;
- Django получает настройки из переменных окружения;
- `DJANGO_DEBUG` выключается в контейнерном запуске;
- `ALLOWED_HOSTS` настраивается через `DJANGO_ALLOWED_HOSTS`;
- SQLite-база хранится в volume `catalog_db`, а не внутри слоя контейнера;
- статические файлы собираются в volume `static_files`;
- nginx отдает `/static/` из общего static volume;
- entrypoint выполняет миграции;
- entrypoint выполняет `collectstatic`;
- entrypoint загружает фикстуру `battery_catalog`;
- линтер `pycodestyle` проходит без ошибок;
- Django-тесты проходят в контейнере без ошибок;
- функциональность из ПЗ6 сохраняется: каталог, формы, роли, партии и расчеты работают.

# Features NOT to be tested

На этом этапе не проверяются:

- деплой на внешний сервер или облачную платформу;
- HTTPS/TLS-сертификаты;
- production-секреты и secret manager;
- PostgreSQL, так как в проекте используется SQLite с Docker volume;
- нагрузочное тестирование;
- горизонтальное масштабирование;
- CI/CD pipeline;
- резервное копирование volume;
- мониторинг и логирование в production-системах;
- безопасность nginx за пределами учебного окружения.

# Approach

Проверка выполняется через Docker Compose и стандартные команды Django:

- `docker compose build` проверяет сборку образа;
- `docker compose up -d` запускает связку `web` + `nginx`;
- HTTP-запрос к `http://127.0.0.1:8087/` проверяет доступность приложения через nginx;
- `docker compose ps` проверяет, что контейнеры находятся в состоянии `Up`;
- команда внутри `web` проверяет наличие файла `/data/db.sqlite3`;
- `docker compose run --rm --no-deps --entrypoint= web pycodestyle .` проверяет PEP8;
- `docker compose run --rm --no-deps --entrypoint= web python manage.py test catalog.tests --verbosity=1` запускает тесты в контейнере.

Для кода Django сохраняется тестовый набор из ПЗ6:

- маршруты;
- отображение каталога;
- формы товара;
- права доступа;
- партии на отправку;
- расчет суммы партии.

# Item Pass/Fail Criteria

Проверка считается пройденной, если выполняются условия:

- Docker-образ собирается без ошибок;
- сервисы `web` и `nginx` запускаются;
- приложение отвечает через nginx со статусом HTTP 200;
- база данных создается по пути `/data/db.sqlite3`;
- `/data` подключен как Docker volume;
- статика собирается в `/static`;
- `/static` подключен к nginx как read-only volume;
- `pycodestyle` завершается с exit code `0`;
- Django-тесты завершаются с exit code `0`;
- все 46 тестов проходят без ошибок.

Проверка считается проваленной, если образ не собирается, контейнеры не стартуют, nginx не проксирует запросы, база создается внутри контейнера вместо volume, линтер возвращает ошибки или хотя бы один Django-тест падает.

# Suspension Criteria

Тестирование нужно приостановить, если:

- Docker daemon недоступен;
- не выполняется `docker compose build`;
- контейнер `web` не стартует из-за ошибки зависимостей;
- миграции не применяются;
- nginx не может подключиться к `web:8000`;
- падает больше 30% Django-тестов;
- линтер не запускается из-за отсутствия зависимости `pycodestyle`.

# Test Deliverables

К сдаче относятся:

- `Dockerfile`;
- `docker-compose.yml`;
- `nginx/default.conf`;
- `scripts/entrypoint.sh`;
- `requirements.txt`;
- `setup.cfg`;
- исходный код Django-проекта;
- пакет тестов `catalog/tests`;
- файл `TEST_PLAN.md`;
- отчет `ПЗ7/ОТЧЕТ.md`;
- скриншот успешного запуска линтера `ПЗ7/screenshots/pz7_linter_ok.png`;
- скриншот успешного запуска тестов `ПЗ7/screenshots/pz7_tests_ok.png`;
- вывод команды линтера в контейнере;
- вывод команды тестов в контейнере.

# Test Case Matrix

| ID | Сценарий | Команда/объект | Ожидаемый результат | Приоритет |
| --- | --- | --- | --- | --- |
| TC-01 | Сборка Docker-образа | `docker compose build` | Образ `pz7-catalog-web` собран без ошибок | High |
| TC-02 | Запуск контейнеров | `docker compose up -d` | Запущены сервисы `web` и `nginx` | High |
| TC-03 | Проверка статуса контейнеров | `docker compose ps` | Контейнеры находятся в состоянии `Up` | High |
| TC-04 | Доступность через nginx | `http://127.0.0.1:8087/` | HTTP 200 | High |
| TC-05 | Django работает через WSGI | `Dockerfile CMD` | Запускается `gunicorn catalog_project.wsgi:application` | High |
| TC-06 | nginx проксирует в Django | `nginx/default.conf` | `proxy_pass http://django_app` ведет на `web:8000` | High |
| TC-07 | База вынесена в volume | `catalog_db:/data` | SQLite создается как `/data/db.sqlite3` | High |
| TC-08 | Проверка файла базы | `ls -l /data && test -f /data/db.sqlite3` | Выводится `DB_FILE_OK` | High |
| TC-09 | Статика вынесена в volume | `static_files:/static` | Django и nginx используют общий static volume | Medium |
| TC-10 | nginx отдает статику | `location /static/` | `/static/` обслуживается через `alias /static/` | Medium |
| TC-11 | Миграции при старте | `entrypoint.sh` | Выполняется `python manage.py migrate --noinput` | High |
| TC-12 | Сбор статики при старте | `entrypoint.sh` | Выполняется `python manage.py collectstatic --noinput` | Medium |
| TC-13 | Загрузка фикстуры | `entrypoint.sh` | Выполняется `python manage.py loaddata battery_catalog` | Medium |
| TC-14 | DEBUG выключен | `DJANGO_DEBUG=False` | В контейнере `DEBUG=False` | High |
| TC-15 | ALLOWED_HOSTS из env | `DJANGO_ALLOWED_HOSTS` | Хосты берутся из переменной окружения | Medium |
| TC-16 | Линтер в контейнере | `docker compose run ... pycodestyle .` | Exit code 0, status OK | High |
| TC-17 | Тесты в контейнере | `docker compose run ... python manage.py test ...` | 46 тестов, OK | High |
| TC-18 | Настройки pycodestyle | `setup.cfg` | `max-line-length = 120`, исключены миграции и кэш | Medium |
| TC-19 | Проверка зависимостей | `requirements.txt` | Есть `Django`, `gunicorn`, `pycodestyle` | Medium |
| TC-20 | Каталог после запуска | `/` через nginx | Список товаров открывается | High |
| TC-21 | Карточка товара после запуска | `/product/<pk>/` через nginx | Карточка товара открывается | Medium |
| TC-22 | Формы и роли не сломаны | `catalog.tests` | Тесты ролей и форм проходят | High |
| TC-23 | Остановка контейнеров | `docker compose down` | Контейнеры остановлены без ошибки | Medium |

# Verification Report

Команда сборки образа:

```bash
docker compose build
```

Команда запуска приложения:

```bash
docker compose up -d
```

Проверка приложения через nginx:

```bash
Invoke-WebRequest -Uri 'http://127.0.0.1:8087/' -UseBasicParsing
```

Ожидаемый результат:

```text
HTTP 200
```

Проверка базы данных во внешнем volume:

```bash
docker compose exec -T web sh -c "ls -l /data && test -f /data/db.sqlite3 && echo DB_FILE_OK"
```

Ожидаемый результат:

```text
DB_FILE_OK
```

Команда запуска линтера в контейнере:

```bash
docker compose run --rm --no-deps --entrypoint= web pycodestyle .
```

Фактический результат по отчету:

```text
exit code: 0
pycodestyle status: OK
```

Команда запуска тестов в контейнере:

```bash
docker compose run --rm --no-deps --entrypoint= web python manage.py test catalog.tests --verbosity=1
```

Фактический результат по отчету:

```text
Found 46 test(s).
Ran 46 tests.
OK
tests status: OK
```

Примечание по локальной проверке: для сдачи ПЗ7 основная проверка должна выполняться именно в контейнере, потому что `Dockerfile` использует Python 3.12. В текущем локальном окружении доступен только Python 3.14, а он не является целевой версией для `Django==4.2.11`; поэтому локальный запуск тестов не заменяет контейнерную проверку. Локальный запуск `pycodestyle .` на зависимостях из `requirements.txt` завершается без ошибок.

# Краткий вывод

ПЗ7 выполняет требования методички: для Django-каталога добавлены Dockerfile, docker-compose, nginx, gunicorn, volume для базы данных и volume для статики. Проект можно поднять как связку `nginx + Django`, а качество подтверждается линтером и тестами в контейнере.
