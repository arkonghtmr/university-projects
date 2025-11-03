import sys
from lxml import etree

def validate_xml(xsd_path, xml_path):
    """
    Функция для валидации XML файла по XSD схеме.
    """
    try:
        # Загружаем XSD схему
        with open(xsd_path, 'rb') as f:
            schema_doc = etree.XML(f.read())
        schema = etree.XMLSchema(schema_doc)
        print(f"✅ Схема '{xsd_path}' успешно загружена.")

        # Загружаем XML документ для проверки
        with open(xml_path, 'rb') as f:
            xml_doc = etree.XML(f.read())
        print(f"🔄 Проверяем файл: '{xml_path}'...")

        # Выполняем валидацию
        schema.assertValid(xml_doc)
        print(f"🎉 SUCCESS: Файл '{xml_path}' соответствует схеме.")

    except etree.XMLSchemaParseError as e:
        print(f"❌ ERROR: Ошибка парсинга XSD схемы: {e}")
    except etree.DocumentInvalid as e:
        print(f"❌ FAILED: Файл '{xml_path}' НЕ соответствует схеме.")
        print("🔍 Детали ошибки:")
        for error in e.error_log:
            print(f"  - Строка {error.line}, колонка {error.column}: {error.message}")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python validator.py <путь_к_схеме.xsd> <путь_к_файлу.xml>")
        sys.exit(1)

    xsd_file = sys.argv[1]
    xml_file = sys.argv[2]
    validate_xml(xsd_file, xml_file)