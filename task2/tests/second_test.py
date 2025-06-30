import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from task2 import ParserConfig, WikipediaAnimalParser, CSVWriter
import csv
import os
import requests


class TestWikipediaAnimalParser(unittest.TestCase):
    def setUp(self):
        self.config = ParserConfig()
        self.parser = WikipediaAnimalParser(self.config)

    @patch('requests.Session.get')
    def test_fetch_page_success(self, mock_get):
        """Тест успешной загрузки страницы"""
        mock_response = MagicMock()
        mock_response.content = '<html><body>Test</body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.parser._fetch_page("http://test.com")
        self.assertIsInstance(result, BeautifulSoup)
        self.assertEqual(result.body.text, 'Test')

    @patch('requests.Session.get')
    def test_fetch_page_failure(self, mock_get):
        """Тест ошибки при загрузке страницы"""
        mock_get.side_effect = requests.RequestException("Connection error")
        result = self.parser._fetch_page("http://test.com")
        self.assertIsNone(result)

    def test_parse_letters(self):
        """Тест извлечения букв из HTML"""
        html = """
        <div class="mw-category-group">
            <ul>
                <li><a>Аист</a></li>
                <li><a>Барсук</a></li>
                <li><a>Волк</a></li>
            </ul>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser._parse_letters(soup)
        self.assertEqual(result, ['А', 'Б', 'В'])

    def test_get_next_page_url_found(self):
        """Тест поиска URL следующей страницы (когда есть)"""
        html = '<a href="/next">Следующая страница</a>'
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser._get_next_page_url(soup)
        self.assertEqual(result, "https://ru.wikipedia.org/next")

    def test_get_next_page_url_not_found(self):
        """Тест поиска URL следующей страницы (когда нет)"""
        html = '<div>No next page</div>'
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser._get_next_page_url(soup)
        self.assertIsNone(result)

    @patch.object(WikipediaAnimalParser, '_fetch_page')
    @patch.object(WikipediaAnimalParser, '_parse_letters')
    @patch.object(WikipediaAnimalParser, '_get_next_page_url')
    def test_get_animal_counts(self, mock_next, mock_parse, mock_fetch):
        """Тест сбора статистики по животным"""
        mock_soup = MagicMock()
        mock_fetch.return_value = mock_soup
        mock_parse.side_effect = [['А', 'Б'], ['В']]
        mock_next.side_effect = ["http://page2", None]

        result = self.parser.get_animal_counts()
        self.assertEqual(result, {'А': 1, 'Б': 1, 'В': 1})
        self.assertEqual(mock_fetch.call_count, 2)


class TestCSVWriter(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_output.csv"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_csv_writer(self):
        """Тест записи данных в CSV"""
        test_data = {'А': 10, 'Б': 5, 'В': 3}
        CSVWriter.write(test_data, self.test_filename)

        self.assertTrue(os.path.exists(self.test_filename))

        with open(self.test_filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        expected = [['А', '10'], ['Б', '5'], ['В', '3']]
        self.assertEqual(sorted(rows), sorted(expected))


class IntegrationTest(unittest.TestCase):
    @patch('requests.Session.get')
    def test_integration(self, mock_get):
        """Интеграционный тест всего пайплайна"""
        mock_response1 = MagicMock()
        mock_response1.content = """
        <div class="mw-category-group">
            <ul>
                <li><a>Аист</a></li>
                <li><a>Барсук</a></li>
            </ul>
            <a href="/next">Следующая страница</a>
        </div>
        """
        mock_response1.raise_for_status.return_value = None

        mock_response2 = MagicMock()
        mock_response2.content = """
        <div class="mw-category-group">
            <ul>
                <li><a>Волк</a></li>
            </ul>
        </div>
        """
        mock_response2.raise_for_status.return_value = None

        mock_get.side_effect = [mock_response1, mock_response2]

        parser = WikipediaAnimalParser()
        counts = parser.get_animal_counts()

        self.assertEqual(counts, {'А': 1, 'Б': 1, 'В': 1})


if __name__ == '__main__':
    unittest.main()
