import redis
import sys
import json
import time

# Подключение к Redis
# decode_responses=True, чтобы получать строки, а не байты
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def add_task_to_queue(task_description: str):
    """
    Формирует задачу и добавляет ее в очередь Redis.
    """
    task_id = int(time.time() * 1000)  # Простой уникальный ID на основе времени
    task_data = {
        'id': task_id,
        'description': task_description,
        'status': 'new'
    }

    # Конвертируем словарь в JSON-строку
    task_json = json.dumps(task_data)

    # Добавляем задачу в начало списка (очереди)
    r.lpush('tasks_queue', task_json)

    print(f"Задача добавлена в очередь. ID: {task_id}, Описание: '{task_description}'")


if __name__ == "__main__":
    # Получаем описание задачи из аргументов командной строки
    if len(sys.argv) > 1:
        description = sys.argv[1]
        add_task_to_queue(description)
    else:
        print("Ошибка: Необходимо передать описание задачи в качестве аргумента.")
        print("Пример: python producer.py \"Сгенерировать отчет\"")