import csv
import random
from faker import Faker
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import defaultdict
import os

# Генерирую данные
print("Шаг 1: Генерация данных...")
fake = Faker('ru_RU')


def create_review(user_ids):
    return {'user_id': random.choice(user_ids), 'text': fake.text(max_nb_chars=200)}


def create_publication(user_ids):
    return {
        'title': fake.sentence(nb_words=5), 'description': fake.text(max_nb_chars=500),
        'pages': random.randint(1, 100), 'category': fake.word(),
        'publication_date': fake.date_time_this_decade().isoformat(),
        'reviews': [create_review(user_ids) for _ in range(random.randint(0, 3))]
    }


def create_user(user_id):
    return {
        'id': user_id, 'name': fake.name(),
        'emails': [fake.email() for _ in range(random.randint(1, 3))],
        'registration_date': fake.date_time_this_decade().isoformat(),
        'last_login_date': fake.date_time_this_year().isoformat(),
        'account_status_confirmed': random.choice([True, False]),
        'birth_date': fake.date_of_birth(minimum_age=10, maximum_age=80).isoformat(),
        'gender': random.choice(['Мужской', 'Женский']), 'publications': []
    }


num_users = 1000
users_data = [create_user(i) for i in range(1, num_users + 1)]
user_ids = [user['id'] for user in users_data]
for user in users_data:
    user['publications'] = [create_publication(user_ids) for _ in range(random.randint(1, 4))]
print(f"Сгенерировано {len(users_data)} записей о пользователях.")

# Сохраняю данные в XML
print("\nШаг 2: Сохранение данных в формате XML...")
root = ET.Element('users')
for user_dict in users_data:
    user_element = ET.SubElement(root, 'user', id=str(user_dict['id']))
    ET.SubElement(user_element, 'name').text = user_dict['name']
    ET.SubElement(user_element, 'registration_date').text = user_dict['registration_date']
    ET.SubElement(user_element, 'last_login_date').text = user_dict['last_login_date']
    ET.SubElement(user_element, 'account_status_confirmed').text = str(user_dict['account_status_confirmed'])
    ET.SubElement(user_element, 'birth_date').text = user_dict['birth_date']
    ET.SubElement(user_element, 'gender').text = user_dict['gender']
    emails_element = ET.SubElement(user_element, 'emails')
    for email in user_dict['emails']:
        ET.SubElement(emails_element, 'email').text = email
    publications_element = ET.SubElement(user_element, 'publications')
    for pub_dict in user_dict['publications']:
        pub_element = ET.SubElement(publications_element, 'publication')
        ET.SubElement(pub_element, 'title').text = pub_dict['title']
        ET.SubElement(pub_element, 'description').text = pub_dict['description']
        ET.SubElement(pub_element, 'pages').text = str(pub_dict['pages'])
        ET.SubElement(pub_element, 'category').text = pub_dict['category']
        ET.SubElement(pub_element, 'publication_date').text = pub_dict['publication_date']
        reviews_element = ET.SubElement(pub_element, 'reviews')
        for review_dict in pub_dict['reviews']:
            review_element = ET.SubElement(reviews_element, 'review')
            ET.SubElement(review_element, 'user_id').text = str(review_dict['user_id'])
            ET.SubElement(review_element, 'text').text = review_dict['text']
xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
xml_filename = 'users_data.xml'
with open(xml_filename, 'w', encoding='utf-8') as f:
    f.write(xml_string)
print(f"Данные успешно сохранены в файл '{xml_filename}'.")

# Чтение данных в xml и преобразование
print("\nШаг 3: Чтение данных из XML и применение преобразования...")
tree = ET.parse(xml_filename)
root = tree.getroot()
user_id_to_name_map = {user.get('id'): user.find('name').text for user in root.findall('user')}
for user in root.findall('user'):
    for publication in user.find('publications'):
        for review in publication.find('reviews'):
            reviewer_id = review.find('user_id').text
            reviewer_name = user_id_to_name_map.get(reviewer_id, "Неизвестный пользователь")
            ET.SubElement(review, 'reviewer_name').text = reviewer_name
print("Преобразование успешно выполнено: к каждому отзыву добавлено имя автора.")

# сохраняю в DSV 
print("\nШаг 4: Сохранение преобразованных данных в единый файл DSV (с разделителем-табуляцией)...")

dsv_filename_single = 'users_data_transformed.dsv'

headers = [
    'user_id', 'user_name', 'user_emails', 'registration_date', 'last_login_date',
    'account_status_confirmed', 'birth_date', 'gender', 'publication_title',
    'publication_description', 'publication_pages', 'publication_category',
    'publication_date', 'publication_reviews'
]

with open(dsv_filename_single, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    for user in root.findall('user'):
        user_info = [
            user.get('id'), user.find('name').text,
            ';'.join([email.text for email in user.find('emails')]),
            user.find('registration_date').text, user.find('last_login_date').text,
            user.find('account_status_confirmed').text, user.find('birth_date').text,
            user.find('gender').text
        ]
        for publication in user.find('publications'):
            reviews_list = []
            for review in publication.find('reviews'):
                reviewer_name = review.find('reviewer_name').text
                review_text = review.find('text').text

                # ИСПРАВЛЕНИЕ: Квадратные скобки полностью убраны из форматирования
                reviews_list.append(f"{reviewer_name}: {review_text}")

            reviews_str = '\n'.join(reviews_list)

            publication_info = [
                publication.find('title').text,
                publication.find('description').text,
                publication.find('pages').text, publication.find('category').text,
                publication.find('publication_date').text, reviews_str
            ]
            writer.writerow(user_info + publication_info)
print(f"Преобразованные данные успешно сохранены в файл '{dsv_filename_single}'.")

print(f"\nШаг 5: Разделение файла '{dsv_filename_single}' на несколько файлов по году регистрации...")

data_by_year = defaultdict(list)

# Читаю созданный файл
with open(dsv_filename_single, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_ALL)

    header_row = next(reader)
    registration_date_index = header_row.index('registration_date')

    # Группирую данные
    for row in reader:
        registration_date_str = row[registration_date_index]
        year = registration_date_str[:4]
        data_by_year[year].append(row)

print("Данные сгруппированы по годам. Начинаю запись файлов...")

output_dir = 'split_dsv_files'
os.makedirs(output_dir, exist_ok=True)

for year, rows in data_by_year.items():
    output_filename = os.path.join(output_dir, f'users_registered_{year}.dsv')

    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL)
        writer.writerow(header_row)
        writer.writerows(rows)
    print(f" -> Создан файл: '{output_filename}' (записей: {len(rows)})")

print(f"\nПрактическая работа завершена. Разделенные файлы находятся в папке '{output_dir}'.")