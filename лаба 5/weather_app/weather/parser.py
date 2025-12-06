"""
Модуль для обработки аргументов командной строки.

Предоставляет функциональность для создания и настройки парсера
аргументов командной строки с помощью библиотеки argparse.
"""

import argparse
from typing import List


def create_parser() -> argparse.ArgumentParser:
    """
    Создает и настраивает парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: Настроенный объект парсера
    """
    parser = argparse.ArgumentParser(
        description="Консольное приложение для получения информации о погоде",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --city "Москва"
  python main.py --city "Санкт-Петербург" --format detailed
  python main.py --city "Казань" --force
  python main.py --clear-cache
        """
    )

    # Основная группа аргументов
    parser.add_argument(
        "-c", "--city",
        type=str,
        help="Название города для получения информации о погоде",
        metavar="ГОРОД"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["short", "detailed"],
        default="short",
        help="Формат вывода информации (краткий или подробный)",
        metavar="ФОРМАТ"
    )

    # Флаги
    parser.add_argument(
        "--force",
        action="store_true",
        help="Принудительное обновление данных (игнорировать кэш)"
    )

    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Очистить кэш данных о погоде"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser


def validate_args(args: argparse.Namespace) -> List[str]:
    """
    Проверяет корректность аргументов командной строки.

    Args:
        args (argparse.Namespace): Аргументы командной строки

    Returns:
        List[str]: Список сообщений об ошибках (пустой, если ошибок нет)
    """
    errors = []

    # Проверяем, что указан город, если не выполняется очистка кэша
    if not args.clear_cache and not args.city:
        errors.append("Не указан город. Используйте --city ГОРОД")

    # Проверяем формат названия города
    if args.city and len(args.city.strip()) < 2:
        errors.append("Название города должно содержать не менее 2 символов")

    return errors