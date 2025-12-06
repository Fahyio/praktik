"""
Скрипт для тестирования документации проекта.
"""

import weather
from weather import models, api, cache, parser, commands


def test_module_docs():
    """Тестирует документацию модулей."""
    print("=== Тестирование документации модулей ===\n")

    modules = [weather, models, api, cache, parser, commands]

    for module in modules:
        print(f"Модуль: {module.__name__}")
        print("-" * 40)
        if module.__doc__:
            print(module.__doc__.strip())
        else:
            print("Документация отсутствует")
        print("\n")


def test_function_docs():
    """Тестирует документацию функций и классов."""
    print("=== Тестирование документации классов и методов ===\n")

    # Тестируем класс WeatherData
    print("Класс: WeatherData")
    print("-" * 40)
    print(help(models.WeatherData))

    # Тестируем метод to_dict
    print("\nМетод: WeatherData.to_dict")
    print("-" * 40)
    print(help(models.WeatherData.to_dict))

    # Тестируем функцию create_parser
    print("\nФункция: create_parser")
    print("-" * 40)
    print(help(parser.create_parser))


def test_package_docs():
    """Тестирует документацию пакета."""
    print("=== Тестирование документации пакета ===\n")
    print(help(weather))


if __name__ == "__main__":
    print("Тестирование документации проекта 'Погода'\n")

    test_package_docs()
    test_module_docs()
    test_function_docs()

    print("\nТестирование завершено!")