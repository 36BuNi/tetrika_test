from functools import wraps
from typing import Any, Callable, TypeVar, cast
from inspect import signature

F = TypeVar('F', bound=Callable[..., Any])


def strict(func: F) -> F:
    """
    Декоратор для строгой проверки типов аргументов. Возвращаемый тип не проверяется.


    :param func: Декорируемая функция.
    :return: Декорированная функция с проверкой типов.

    :raises TypeError: Если аргумент не соответствует аннотации или количество аргументов не совпадает с ожидаемым.
    """

    sig = signature(func)
    annotations = func.__annotations__

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be of type {expected_type.__name__}, "
                        f"got {type(value).__name__} instead"
                    )

        return func(*args, **kwargs)

    return cast(F, wrapper)
