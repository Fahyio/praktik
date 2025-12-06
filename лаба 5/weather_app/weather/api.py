"""
Модуль для работы с API погоды.

Предоставляет функциональность для получения данных о погоде
с внешнего API (open-meteo.com).
"""

import requests
import json
from typing import Dict, Optional, Tuple
from datetime import datetime
from .models import WeatherData


class WeatherAPI:
    """
    Класс для взаимодействия с API погоды.

    Attributes:
        BASE_URL (str): Базовый URL API
        TIMEOUT (int): Таймаут запросов в секундах
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    TIMEOUT = 10

    def __init__(self, timeout: int = None):
        """
        Инициализирует объект WeatherAPI.

        Args:
            timeout (int, optional): Таймаут для запросов. По умолчанию TIMEOUT.
        """
        self.timeout = timeout or self.TIMEOUT
        self.session = requests.Session()

    def get_city_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        """
        Получает координаты города по его названию.

        Использует геокодинг для преобразования названия города
        в географические координаты (широта, долгота).

        Args:
            city (str): Название города

        Returns:
            Optional[Tuple[float, float]]: Кортеж (широта, долгота) или None

        Raises:
            ConnectionError: При проблемах с сетью
            TimeoutError: При превышении времени ожидания
        """
        try:
            # Здесь должна быть реализация геокодинга
            # Для примера используем статические координаты
            cities = {
                "москва": (55.7558, 37.6176),
                "санкт-петербург": (59.9343, 30.3351),
                "казань": (55.8304, 49.0661),
                "сочи": (43.5855, 39.7231),
                "екатеринбург": (56.8389, 60.6057)
            }

            city_lower = city.lower()
            if city_lower in cities:
                return cities[city_lower]

            # Если город не найден в списке, используем координаты Москвы как fallback
            return (55.7558, 37.6176)

        except Exception as e:
            raise ConnectionError(f"Ошибка при получении координат: {e}")

    def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Получает текущую погоду для указанного города.

        Args:
            city (str): Название города

        Returns:
            Optional[WeatherData]: Объект с данными о погоде или None

        Raises:
            ValueError: Если город не найден
            ConnectionError: При проблемах с подключением к API
            TimeoutError: При превышении таймаута
        """
        try:
            coordinates = self.get_city_coordinates(city)
            if not coordinates:
                raise ValueError(f"Город '{city}' не найден")

            latitude, longitude = coordinates

            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                           "wind_speed_10m,wind_direction_10m,pressure_msl,weather_code",
                "timezone": "auto"
            }

            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            current = data.get("current", {})

            # Преобразуем код погоды в текстовое описание
            weather_codes = {
                0: "ясно", 1: "преимущественно ясно", 2: "переменная облачность",
                3: "облачно", 45: "туман", 48: "иней", 51: "легкая морось",
                53: "умеренная морось", 55: "сильная морось", 56: "легкий ледяной дождь",
                57: "сильный ледяной дождь", 61: "небольшой дождь", 63: "умеренный дождь",
                65: "сильный дождь", 66: "легкий ледяной дождь", 67: "сильный ледяной дождь",
                71: "небольшой снег", 73: "умеренный снег", 75: "сильный снег",
                77: "снежные зерна", 80: "небольшие ливни", 81: "умеренные ливни",
                82: "сильные ливни", 85: "небольшие снегопады", 86: "сильные снегопады",
                95: "гроза", 96: "гроза с небольшим градом", 99: "гроза с сильным градом"
            }

            weather_code = current.get("weather_code", 0)
            conditions = weather_codes.get(weather_code, "неизвестно")

            return WeatherData(
                city=city,
                temperature=current.get("temperature_2m", 0),
                feels_like=current.get("apparent_temperature", 0),
                humidity=current.get("relative_humidity_2m", 0),
                wind_speed=current.get("wind_speed_10m", 0),
                wind_direction=self._get_wind_direction(current.get("wind_direction_10m")),
                pressure=current.get("pressure_msl", 1013),
                conditions=conditions,
                timestamp=datetime.now()
            )

        except requests.exceptions.Timeout:
            raise TimeoutError("Превышено время ожидания ответа от API")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Ошибка подключения к API погоды")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"Ошибка HTTP: {e}")
        except Exception as e:
            raise ConnectionError(f"Неизвестная ошибка: {e}")

    def _get_wind_direction(self, degrees: float) -> Optional[str]:
        """
        Преобразует направление ветра из градусов в текстовое описание.

        Args:
            degrees (float): Направление в градусах (0-360)

        Returns:
            Optional[str]: Текстовое описание направления
        """
        if degrees is None:
            return None

        directions = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
        index = int((degrees + 22.5) / 45) % 8
        return directions[index]