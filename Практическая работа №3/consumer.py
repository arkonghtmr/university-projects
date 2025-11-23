import redis
import time
import json
import random

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def process_task(task_json: str):
    """
    Имитирует обработку задачи.
    """
    task_data = json.loads(task_json)
    task_id = task_data.get('id')
    description = task_data.get('description')

    print(f"[ВОРКЕР] Получена задача ID:{task_id}. Описание: '{description}'")

    # Имитация долгой работы
    processing_time = random.randint(2, 5)
    print(f"[ВОРКЕР] Обрабатываю... (займет {processing_time} сек.)")
    time.sleep(processing_time)

    print(f"[ВОРКЕР] Задача ID:{task_id} успешно обработана.")


def main_loop():
    """
    Основной цикл воркера, который слушает очередь.
    """
    print("Воркер запущен, ожидаю задач...")
    while True:
        try:
            # BRPOP - блокирующая операция извлечения из конца списка
            # 0 - означает бесконечное ожидание
            # ('tasks_queue', 0) - кортеж, где первый элемент - ключ списка
            task = r.brpop('tasks_queue', 0)

            # brpop возвращает кортеж (имя_очереди, значение)
            if task:
                task_data_json = task[1]
                process_task(task_data_json)

        except redis.exceptions.ConnectionError as e:
            print(f"Ошибка подключения к Redis: {e}. Повторная попытка через 5 секунд...")
            time.sleep(5)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main_loop()