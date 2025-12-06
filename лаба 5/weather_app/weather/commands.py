"""
Модуль обработчиков команд.

Содержит функции для обработки различных команд приложения погоды.
"""

import sys
from typing import Any
from argparse import Namespace
from .api import WeatherAPI
from .cache import WeatherCache
from .parser import validate_args


def handle_command(args: Namespace) -> None:
    """
    Основной обработчик команд приложения.

    Определяет, какую команду выполнить на основе аргументов
    и вызывает соответствующий обработчик.

    Args:
        args (Namespace): Аргументы командной строки

    Raises:
        SystemExit: При ошибках валидации аргументов
    """
    # Проверяем аргументы
    errors = validate_args(args)
    if errors:
        for error in errors:
            print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)

    # Выполняем команду
    if args.clear_cache:
        clear_cache_command()
    elif args.city:
        weather_command(args.city, args.format, args.force)


def weather_command(city: str, output_format: str = "short", force: bool = False) -> None:
    """
    Обработчик команды получения информации о погоде.

    Args:
        city (str): Название города
        output_format (str): Формат вывода (short/detailed)
        force (bool): Принудительное обновление данных

    Raises:
        SystemExit: При критических ошибках
    """
    cache = WeatherCache()
    api = WeatherAPI()

    weather_data = None

    # Пробуем получить данные из кэша, если не принудительное обновление
    if not force:
        weather_data = cache.get(city)

    # Если данных нет в кэше или они устарели, получаем из API
    if not weather_data:
        try:
            weather_data = api.get_weather(city)
            # Сохраняем в кэш
            cache.set(city, weather_data)
        except Exception as e:
            print(f"Ошибка при получении данных: {e}", file=sys.stderr)
            sys.exit(1)

    # Выводим результат
    if output_format == "detailed":
        print_detailed_weather(weather_data)
    else:
        print_short_weather(weather_data)


def clear_cache_command() -> None:
    """
    Обработчик команды очистки кэша.
    """
    cache = WeatherCache()
    cache.clear()


def print_short_weather(weather_data: Any) -> None:
    """
    Выводит краткую информацию о погоде.

    Args:
        weather_data (WeatherData): Данные о погоде
    """
    print(f"\nПогода в {weather_data.city}:")
    print(f"Температура: {weather_data.temperature:+.1f}°C")
    print(f"Влажность: {weather_data.humidity}%")
    print(f"Скорость ветра: {weather_data.wind_speed} м/с")
    print(f"Условия: {weather_data.conditions}")


def print_detailed_weather(weather_data: Any) -> None:
    """
    Выводит подробную информацию о погоде.

    Args:
        weather_data (WeatherData): Данные о погоде
    """
    print(f"\n{'=' * 40}")
    print(f"Детальная информация о погоде")
    print(f"{'=' * 40}")
    print(f"Город: {weather_data.city}")
    print(f"Температура: {weather_data.temperature:+.1f}°C")
    print(f"Ощущается как: {weather_data.feels_like:+.1f}°C")
    print(f"Влажность: {weather_data.humidity}%")
    print(f"Скорость ветра: {weather_data.wind_speed:.1f} м/с")

    if weather_data.wind_direction:
        print(f"Направление ветра: {weather_data.wind_direction}")

    print(f"Атмосферное давление: {weather_data.pressure} гПа")
    print(f"Погодные условия: {weather_data.conditions}")
    print(f"Время обновления: {weather_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 40}")