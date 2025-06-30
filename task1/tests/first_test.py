import unittest
import time

import pytest

from task1 import strict


class StrictDecoratorTestCase(unittest.TestCase):
    """Тесты для декоратора строгой типизации."""

    def test_correct_integer_arguments(self) -> None:
        """Проверяет корректную работу с целыми числами."""

        @strict
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(0, -5), -5)
        self.assertEqual(add(1000, 2000), 3000)

    def test_type_mismatch_raises_error(self) -> None:
        """Проверяет вызов TypeError при несоответствии типов."""

        @strict
        def divide(a: int, b: int) -> float:
            return a / b

        with self.assertRaises(TypeError):
            divide(1.5, 2)

        with self.assertRaises(TypeError):
            divide("1", 2)

        with self.assertRaises(TypeError):
            divide(1, None)

    def test_mixed_argument_types(self) -> None:
        """Проверяет функции с аргументами разных типов."""

        @strict
        def create_profile(name: str, age: int, is_active: bool) -> str:
            return f"{name}, {age}, active: {is_active}"

        self.assertEqual(create_profile("Alabai", 44, True), "Alabai, 44, active: True")

        with self.assertRaises(TypeError):
            create_profile("Barmaley", "333", True)

    def test_argument_count_validation(self) -> None:
        """Проверяет контроль количества аргументов."""

        @strict
        def power(base: int, exponent: int) -> int:
            return base ** exponent

        with self.assertRaises(TypeError):
            power(2)

        with self.assertRaises(TypeError):
            power(2, 3, 4)

    def test_boolean_type(self) -> None:
        """Проверяет строгую проверку булевых значений."""

        @strict
        def invert(flag: bool) -> bool:
            return not flag

        self.assertEqual(invert(True), False)

        with self.assertRaises(TypeError):
            invert(1)

        with self.assertRaises(TypeError):
            invert(None)

    @staticmethod
    def test_float_type() -> None:
        """Проверяет, что требует именно float, а не int/bool."""

        @strict
        def half(x: float) -> float:
            return x / 2

        assert half(1.0) == 0.5
        assert half(3.14) == 1.57

        with pytest.raises(TypeError):
            half(1)

        with pytest.raises(TypeError):
            half(True)

    def test_string_validation(self) -> None:
        """Проверяет обработку строковых аргументов."""

        @strict
        def repeat(text: str, times: int) -> str:
            return text * times

        self.assertEqual(repeat("aa", 3), "aaa")

        with self.assertRaises(TypeError):
            repeat(123, 3)

    def test_none_handling(self) -> None:
        """Проверяет обработку None как отдельного типа."""

        @strict
        def to_upper(text: str) -> str:
            return text.upper()

        with self.assertRaises(TypeError):
            to_upper(None)

    def test_return_type_not_checked(self) -> None:
        """Проверяет, что тип возвращаемого значения не проверяется."""

        @strict
        def bad_function(x: int) -> str:
            return x

        self.assertEqual(bad_function(1), 1)

    def test_performance(self) -> None:
        """Проверяет, что декоратор не добавляет значительных задержек."""

        @strict
        def fast_function(x: int, y: int) -> int:
            return x + y

        start_time = time.time()
        for _ in range(10000):
            fast_function(1, 2)
        end_time = time.time()

        self.assertLess(end_time - start_time, 0.1, "Слишком медленный декоратор")


if __name__ == '__main__':
    unittest.main(verbosity=2)
