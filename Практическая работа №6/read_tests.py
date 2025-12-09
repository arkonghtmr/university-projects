import time
import psycopg2
from statistics import mean


PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "timeseries"
PG_USER = "postgres"
PG_PASS = "postgres"

ITERATIONS = 20  # количество итераций для каждого теста

def get_row_count(table):
    # получаем количество строк в указанной таблице
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASS
    )
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

def run_tests_avg():
    
    tables = {
        "sensor_data_pg": "PostgreSQL",
        "sensor_data_ts": "TimescaleDB"
    }

    #  количество строк в каждой таблице
    for t, label in tables.items():
        print(f"{label}: {get_row_count(t)} строк")
    print()

    # запрос 1: простой фильтр по времени и sensor_id
    query1 = """
        SELECT * FROM {TABLE}
        WHERE sensor_id = 1 AND time > NOW() - INTERVAL '1 hour';
    """

    # запрос 2: агрегация по 10-минутным интервалам за сутки
    query2 = """
        SELECT
            date_trunc('hour', time) +
            floor(extract(minute from time) / 10) * interval '10 minute' AS t10,
            AVG(temperature)
        FROM {TABLE}
        WHERE sensor_id = 1 AND time > NOW() - INTERVAL '24 hours'
        GROUP BY t10
        ORDER BY t10 DESC;
    """

    # запрос 3: крупная агрегация за 30 дней 30 мин
    query3_pg = """
        SELECT
            date_trunc('hour', time) +
            floor(extract(minute from time) / 30) * interval '30 minute' AS t30,
            AVG(temperature)
        FROM sensor_data_pg
        WHERE time > NOW() - INTERVAL '30 days'
        GROUP BY t30;
    """
    query3_ts = """
        SELECT
            time_bucket('30 minutes', time) AS t30,
            AVG(temperature)
        FROM sensor_data_ts
        WHERE time > NOW() - INTERVAL '30 days'
        GROUP BY t30;
    """

    results = {}

    for table, label in tables.items():
        times_q1, times_q2, times_q3 = [], [], []

        conn = psycopg2.connect(
            host=PG_HOST, port=PG_PORT, dbname=PG_DB,
            user=PG_USER, password=PG_PASS
        )
        cur = conn.cursor()

        cur.execute(query1.format(TABLE=table)); cur.fetchall()
        cur.execute(query2.format(TABLE=table)); cur.fetchall()

        if table == "sensor_data_pg":
            cur.execute(query3_pg); cur.fetchall()
        else:
            cur.execute(query3_ts); cur.fetchall()

        # запускаем тесты в цикле
        for _ in range(ITERATIONS):
            start = time.time()
            cur.execute(query1.format(TABLE=table))
            cur.fetchall()
            times_q1.append((time.time() - start) * 1000)

            start = time.time()
            cur.execute(query2.format(TABLE=table))
            cur.fetchall()
            times_q2.append((time.time() - start) * 1000)

            start = time.time()
            if table == "sensor_data_pg":
                cur.execute(query3_pg)
            else:
                cur.execute(query3_ts)
            cur.fetchall()
            times_q3.append((time.time() - start) * 1000)

        cur.close()
        conn.close()

        #  среднее время выполнения для каждого запроса
        results[label] = {
            "q1": mean(times_q1),
            "q2": mean(times_q2),
            "q3": mean(times_q3)
        }

    
    print("\n=== Среднее время выполнения, мс ===")
    print(f"Тест 1 — простой диапазон (1 час)")
    print(f"Тест 2 — агрегация по 10 минут (24 часа)")
    print(f"Тест 3 — агрегация 30 минут за 30 дней (TimescaleDB ускорение)\n")

    for label, r in results.items():
        print(f"{label}:")
        print(f"  Запрос 1: {r['q1']:.2f} мс")
        print(f"  Запрос 2: {r['q2']:.2f} мс")
        print(f"  Запрос 3: {r['q3']:.2f} мс\n")

if __name__ == "__main__":
    run_tests_avg()