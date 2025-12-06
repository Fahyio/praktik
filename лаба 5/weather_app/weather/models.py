"""
Модуль моделей данных для приложения погоды.

Содержит классы, описывающие структуру данных о погоде.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeatherData:
    """
    Класс для хранения данных о погоде.

    Attributes:
        city (str): Название города
        temperature (float): Температура в градусах Цельсия
        feels_like (float): Ощущаемая температура
        humidity (int): Влажность в процентах
        wind_speed (float): Скорость ветра в м/с
        wind_direction (Optional[str]): Направление ветра
        pressure (int): Атмосферное давление в гПа
        conditions (str): Описание погодных условий
        timestamp (datetime): Время получения данных
    """

    city: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: Optional[str]
    pressure: int
    conditions: str
    timestamp: datetime

    def to_dict(self) -> dict:
        """
        Преобразует объект WeatherData в словарь.

        Returns:
            dict: Словарь с данными о погоде
        """
        return {
            "city": self.city,
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "pressure": self.pressure,
            "conditions": self.conditions,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'WeatherData':
        """
        Создает объект WeatherData из словаря.

        Args:
            data (dict): Словарь с данными о погоде

        Returns:
            WeatherData: Объект с данными о погоде

        Raises:
            ValueError: Если в словаре отсутствуют обязательные поля
        """
        required_fields = ["city", "temperature", "humidity", "conditions"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        return cls(
            city=data["city"],
            temperature=data["temperature"],
            feels_like=data.get("feels_like", data["temperature"]),
            humidity=data["humidity"],
            wind_speed=data.get("wind_speed", 0),
            wind_direction=data.get("wind_direction"),
            pressure=data.get("pressure", 1013),
            conditions=data["conditions"],
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat()))
        )