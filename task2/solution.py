import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ParserConfig:
    """
    Конфигурация для парсера Wikipedia.

    :param base_url: Базовый URL Wikipedia, default "https://ru.wikipedia.org".
    :param start_url: URL начальной страницы для парсинга, формируется автоматически.
    :param group_selector: CSS-селектор для групп животных, default ".mw-category-group ul li a".
    :param next_page_text: Текст ссылки на следующую страницу, default "Следующая страница".
    :param timeout: Таймаут для HTTP-запросов (с), default 10.
    """
    base_url: str = "https://ru.wikipedia.org"
    start_url: str = f"{base_url}/wiki/Категория:Животные_по_алфавиту"
    group_selector: str = ".mw-category-group ul li a"
    next_page_text: str = "Следующая страница"
    timeout: int = 10


class WikipediaAnimalParser:
    """Парсер для сбора статистики животных с Wikipedia."""

    def __init__(self, config: ParserConfig = ParserConfig()):
        """
        Инициализация парсера с конфигурацией.

        :param config: Конфигурация парсера, без изменений default.
        """

        self.config = config
        self.session = requests.Session()

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Загружает и парсит HTML-страницу.

        :param url: URL для загрузки.
        :return: BeautifulSoup или None при ошибке.
        """

        try:
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException:

            return None

    def _parse_letters(self, soup: BeautifulSoup) -> List[str]:
        """
        Извлекает первые буквы названий животных со страницы.

        :param soup: Объект страницы.
        :return: Список первых букв названий животных.
        """

        return [
            item.text.strip()[0].upper()
            for item in soup.select(self.config.group_selector)
            if item.text.strip()
        ]

    def _get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Находит URL следующей страницы.

        :param soup: Объект страницы.
        :return: URL следующей страницы или None если это последняя.
        """

        next_link = soup.find("a", string=self.config.next_page_text)
        return f"{self.config.base_url}{next_link['href']}" if next_link else None

    def get_animal_counts(self) -> Dict[str, int]:
        """Собирает статистику животных по буквам.

        :return: Сортированный словарь с количеством животных по буквам.
        """

        counts = defaultdict(int)
        next_url = self.config.start_url

        while next_url:
            soup = self._fetch_page(next_url)
            if not soup:
                break

            for letter in self._parse_letters(soup):
                counts[letter] += 1

            next_url = self._get_next_page_url(soup)

        return dict(sorted(counts.items()))


class CSVWriter:
    """Класс для записи данных в CSV файл."""

    @staticmethod
    def write(data: Dict[str, int], filename: str = "beasts.csv") -> None:
        """
        Записывает данные в CSV файл.

        :param data: Данные для записи.
        :param filename: Имя файла для сохранения.
        """

        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data.items())


def main():
    """Основная функция для запуска парсера."""

    parser = WikipediaAnimalParser()
    counts = parser.get_animal_counts()
    CSVWriter.write(counts)


if __name__ == "__main__":
    main()
