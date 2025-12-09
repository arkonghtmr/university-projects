import time
import pandas as pd
import numpy as np
from datetime import timedelta
import psycopg2
from psycopg2.extras import execute_batch
import sys

# конфигурация генерации данных
NUM_RECORDS = 5_000_000  
BATCH_SIZE = 50_000     
NUM_SENSORS = 100        
# настройки подключения к PostgreSQL
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "timeseries"
PG_USER = "postgres"
PG_PASS = "postgres"

def setup_postgres():
    # создаёт/пересоздаёт таблицы; возвращает True, если установлен timescaledb
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS, database=PG_DB
    )
    conn.autocommit = True
    cur = conn.cursor()

    # проверяем, установлено ли расширение timescaledb
    cur.execute("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'timescaledb');")
    has_timescaledb = cur.fetchone()[0]

    # создаём таблицу для timescaledb (если расширение есть)
    cur.execute("DROP TABLE IF EXISTS sensor_data_ts;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data_ts (
            time TIMESTAMPTZ NOT NULL,
            sensor_id INTEGER NOT NULL,
            temperature FLOAT,
            humidity FLOAT
        );
    """)
    if has_timescaledb:
        # преобразуем в гипрертаблицу с интервалом чанков 7 дней
        try:
            cur.execute("SELECT create_hypertable('sensor_data_ts','time', if_not_exists => TRUE, chunk_time_interval => INTERVAL '7 days');")
        except Exception:
            # если не получилось — продолжаем, таблица уже есть
            pass

    # создаём обычную таблицу PostgreSQL
    cur.execute("DROP TABLE IF EXISTS sensor_data_pg;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data_pg (
            time TIMESTAMPTZ NOT NULL,
            sensor_id INTEGER NOT NULL,
            temperature FLOAT,
            humidity FLOAT
        );
    """)

    cur.close()
    conn.close()
    return has_timescaledb

def generate_data():
    # генерируем тестовые данные временных рядов
    end_time = pd.Timestamp.now()
    start_time = end_time - pd.Timedelta(days=30)  # данные за последние 30 дней
    timestamps = pd.date_range(start=start_time, end=end_time, periods=NUM_RECORDS)
    sensor_ids = np.random.randint(1, NUM_SENSORS + 1, NUM_RECORDS)  # случайные ID датчиков
    temperatures = np.round(np.random.uniform(15.0, 30.0, NUM_RECORDS), 2)  # температура 15-30°C
    humidities = np.round(np.random.uniform(40.0, 70.0, NUM_RECORDS), 2)    # влажность 40-70%
    return timestamps, sensor_ids, temperatures, humidities

def write_to_postgres(table_name, timestamps, sensor_ids, temperatures, humidities, is_timescale=False):
    # записываем данные в PostgreSQL пакетами
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS, database=PG_DB
    )
    conn.autocommit = False
    cur = conn.cursor()

    # очищаем таблицу перед записью
    cur.execute(f"TRUNCATE TABLE {table_name};")
    conn.commit()

    total_batches = NUM_RECORDS // BATCH_SIZE + (1 if NUM_RECORDS % BATCH_SIZE else 0)
    start_time = time.time()

    last_printed_percent = -1.0
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, NUM_RECORDS)

        #  пакет данных для вставки
        batch_data = []
        for i in range(start_idx, end_idx):
            batch_data.append((
                timestamps[i].to_pydatetime(),
                int(sensor_ids[i]),
                float(temperatures[i]),
                float(humidities[i])
            ))

        #  пакетная вставку
        execute_batch(
            cur,
            f"INSERT INTO {table_name} (time, sensor_id, temperature, humidity) VALUES (%s, %s, %s, %s)",
            batch_data,
            page_size=BATCH_SIZE
        )
        conn.commit()

        #  прогресс в процентах
        progress = (batch_num + 1) / total_batches * 100.0
        if batch_num % max(1, total_batches // 20) == 0 or batch_num == total_batches - 1:
            percent = round(progress, 1)
            if percent != last_printed_percent:
                print(f"{percent}%")
                sys.stdout.flush()
                last_printed_percent = percent

    #  индексы для ускорения запросов
    if is_timescale:
        # индексы для timescaledb
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_time ON {table_name}(time DESC);")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_sensor ON {table_name}(sensor_id, time DESC);")
    else:
        # индексы для PostgreSQL
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_time ON {table_name}(time);")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_sensor ON {table_name}(sensor_id);")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_composite ON {table_name}(sensor_id, time DESC);")
    conn.commit()

    cur.close()
    conn.close()

def main():
  
    has_ts = setup_postgres()
    
    
    timestamps, sensor_ids, temperatures, humidities = generate_data()

    # записываем в PostgreSQL
    write_to_postgres("sensor_data_pg", timestamps, sensor_ids, temperatures, humidities, is_timescale=False)

    # записываем данные в таблицу timescaledb 
    if has_ts:
        write_to_postgres("sensor_data_ts", timestamps, sensor_ids, temperatures, humidities, is_timescale=True)

if __name__ == "__main__":
    main()