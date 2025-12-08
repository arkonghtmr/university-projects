import os
from lxml import etree


def validate_xml(xml_path, xsd_path):
    print(f"Проверка файла: '{xml_path}'...")

    is_valid = True

    if not os.path.exists(xml_path):
        print(f"Ошибка: Файл '{xml_path}' не найден.")
        return False

    if os.path.getsize(xml_path) == 0:
        print(f"Ошибка: Файл '{xml_path}' абсолютно пуст.")
        return False

    try:
        try:
            with open(xsd_path, 'rb') as f:
                schema_doc = etree.XML(f.read())
            schema = etree.XMLSchema(schema_doc)
        except etree.XMLSyntaxError as e:
            print(f"Критическая ошибка в XSD схеме:\n{e}")
            return False


        with open(xml_path, 'rb') as f:
            xml_doc = etree.XML(f.read())


        empty_errors = []
        for element in xml_doc.iter():
            if len(element) == 0:
                text = element.text
                if text is None or not text.strip():
                    empty_errors.append(f"Строка {element.sourceline}: Тег <{element.tag}> пуст.")

        if empty_errors:
            print(f"Найдены пустые значения:")
            for msg in empty_errors:
                print(f"{msg}")
            is_valid = False

        try:
            schema.assertValid(xml_doc)
        except etree.DocumentInvalid:
            print(f"Ошибки несоответствия схеме XSD:")
            for error in schema.error_log:
                print(f"Строка {error.line}: {error.message}")
            is_valid = False

        if is_valid:
            print(f"Документ корректен.")
            return True
        else:
            print(f"Документ содержит ошибки.")
            return False

    except etree.XMLSyntaxError as e:
        print(f"Ошибка синтаксиса XML (файл не читается):")
        print(f"{e}")
        return False

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return False

if __name__ == "__main__":
    XSD_FILE = "survey_schema.xsd"

    print("=== ПРОВЕРКА ФАЙЛОВ ===\n")

    validate_xml("correct_survey.xml", XSD_FILE)
    print("-" * 60)

    validate_xml("incorrect_survey_1.xml", XSD_FILE)
    print("-" * 60)

    validate_xml("incorrect_survey_2.xml", XSD_FILE)

    print("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===")