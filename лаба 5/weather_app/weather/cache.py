"""
Модуль для кэширования данных о погоде.

Предоставляет функциональность для временного хранения данных о погоде
в локальном файле для уменьшения количества запросов к внешнему API.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from .models import WeatherData


class WeatherCache:
    """
    Класс для управления кэшем данных о погоде.

    Attributes:
        cache_file (str): Путь к файлу кэша
        ttl (timedelta): Время жизни кэшированных данных
    """

    def __init__(self, cache_file: str = "weather_cache.json", ttl_minutes: int = 30):
        """
        Инициализирует объект WeatherCache.

        Args:
            cache_file (str): Имя файла для хранения кэша
            ttl_minutes (int): Время жизни данных в минутах
        """
        self.cache_file = cache_file
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self, city: str) -> Optional[WeatherData]:
        """
        Получает данные о погоде из кэша.

        Проверяет наличие данных в кэше и их актуальность
        по времени жизни (TTL).

        Args:
            city (str): Название города

        Returns:
            Optional[WeatherData]: Объект с данными о погоде или None,
                                  если данных нет или они устарели

        Raises:
            IOError: При ошибках чтения файла
            json.JSONDecodeError: При ошибках парсинга JSON
        """
        try:
            if not os.path.exists(self.cache_file):
                return None

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            city_key = city.lower()
            if city_key not in cache_data:
                return None

            cached_item = cache_data[city_key]
            cached_time = datetime.fromisoformat(cached_item["timestamp"])

            # Проверяем актуальность данных
            if datetime.now() - cached_time > self.ttl:
                # Удаляем устаревшие данные
                self._remove_from_cache(city_key)
                return None

            return WeatherData.from_dict(cached_item)

        except (IOError, json.JSONDecodeError) as e:
            # При ошибках чтения кэша считаем его недействительным
            print(f"Внимание: ошибка чтения кэша: {e}")
            return None

    def set(self, city: str, weather_data: WeatherData) -> None:
        """
        Сохраняет данные о погоде в кэш.

        Args:
            city (str): Название города
            weather_data (WeatherData): Данные о погоде

        Raises:
            IOError: При ошибках записи в файл
        """
        try:
            # Загружаем существующий кэш или создаем новый
            cache_data = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

            # Обновляем данные для города
            city_key = city.lower()
            cache_data[city_key] = weather_data.to_dict()

            # Сохраняем обновленный кэш
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)

        except IOError as e:
            print(f"Внимание: не удалось сохранить данные в кэш: {e}")

    def clear(self) -> None:
        """
        Полностью очищает кэш.

        Удаляет файл кэша, если он существует.

        Raises:
            IOError: При ошибках удаления файла
        """
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("Кэш успешно очищен.")
            else:
                print("Файл кэша не существует.")
        except IOError as e:
            print(f"Ошибка при очистке кэша: {e}")

    def _remove_from_cache(self, city_key: str) -> None:
        """
        Удаляет данные для конкретного города из кэша.

        Внутренний метод для удаления устаревших данных.

        Args:
            city_key (str): Ключ города в кэше
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                if city_key in cache_data:
                    del cache_data[city_key]

                    with open(self.cache_file, 'w', encoding='utf-8') as f:
                        json.dump(cache_data, f, ensure_ascii=False, indent=2)

        except (IOError, json.JSONDecodeError):
            # Если произошла ошибка, просто игнорируем
            pass