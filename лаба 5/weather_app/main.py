#!/usr/bin/env python3
"""
Главный модуль консольного приложения для получения информации о погоде.

Модуль обрабатывает аргументы командной строки и делегирует выполнение
команд соответствующим обработчикам из пакета weather.

Примеры использования:
    python main.py --city "Москва"
    python main.py --city "Санкт-Петербург" --format detailed
    python main.py --clear-cache
"""

import argparse
import sys
from weather.commands import handle_command
from weather.parser import create_parser


def main() -> None:
    """
    Основная точка входа в приложение.

    Обрабатывает аргументы командной строки и вызывает соответствующий обработчик.
    В случае возникновения ошибок выводит сообщение и завершает работу с кодом ошибки.

    Raises:
        SystemExit: При возникновении критических ошибок.
    """
    parser = create_parser()
    args = parser.parse_args()

    try:
        handle_command(args)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()