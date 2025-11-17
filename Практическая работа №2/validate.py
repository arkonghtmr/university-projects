from lxml import etree


def validate_xml(xml_path, xsd_path):
    """
    Функция для валидации XML файла по XSD схеме.

    :param xml_path: Путь к XML файлу для проверки.
    :param xsd_path: Путь к XSD файлу схемы.
    :return: True, если валидация прошла успешно, иначе False.
    """
    try:
        # 1. Загружаем XSD схему
        with open(xsd_path, 'rb') as f:
            schema_doc = etree.XML(f.read())
        schema = etree.XMLSchema(schema_doc)
        print(f"✅ Схема '{xsd_path}' успешно загружена.")

        # 2. Загружаем XML файл для проверки
        with open(xml_path, 'rb') as f:
            xml_doc = etree.XML(f.read())
        print(f"📄 Проверяем файл: '{xml_path}'...")

        # 3. Производим валидацию
        schema.assertValid(xml_doc)

        print(f"🎉 Валидация прошла успешно! Документ '{xml_path}' соответствует схеме.")
        return True

    except etree.XMLSchemaParseError as e:
        print(f"❌ Ошибка парсинга схемы '{xsd_path}':\n{e}")
        return False
    except etree.DocumentInvalid as e:
        print(f"❌ Ошибка валидации! Документ '{xml_path}' не соответствует схеме.")
        print("Детали ошибки:")
        # Выводим подробную информацию об ошибках
        for error in schema.error_log:
            print(f"  - Строка {error.line}, колонка {error.column}: {error.message}")
        return False
    except Exception as e:
        print(f"🚨 Произошла непредвиденная ошибка: {e}")
        return False


# --- Запуск проверки ---
if __name__ == "__main__":
    XSD_FILE = "survey_schema.xsd"

    print("--- Начинаем проверку XML файлов ---")

    print("\n" + "=" * 40)
    validate_xml("correct_survey.xml", XSD_FILE)

    print("\n" + "=" * 40)
    validate_xml("incorrect_survey_1.xml", XSD_FILE)

    print("\n" + "=" * 40)
    validate_xml("incorrect_survey_2.xml", XSD_FILE)

    print("\n--- Проверка завершена ---")