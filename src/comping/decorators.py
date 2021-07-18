from dataclasses import dataclass

from typing import Any


@dataclass
class CompingDescription:
    name: str
    short_help: str
    long_help: str


def description(name: str = "", short: str = "", long: str = ""):
    """A python decorator that applies descriptive attributes to process and action objects.

    Args:
        name: Aliased name of the process or action object. Must be a single word.
            Defaults to the name (__name__) of the object.
        short: Short help description associated with process or action.
        long: Long help description associated with process or action. If a
            long help description is not provided the docsting of wrapped object
            will be used (if available).
    """

    def _wrapper(obj: Any) -> Any:
        obj.__comping__ = CompingDescription(
            name=name, short_help=short, long_help=long
        )
        return obj

    return _wrapper


def get_comping_name(obj: Any) -> str:
    """Returns the aliased name of the process or action object. Defaults to
    the name (__name__) of the object."""
    try:
        text = obj.__comping__.name
        if len(text.split()) > 1:
            raise ValueError("Description 'name' must be a single world")
        return text
    except AttributeError:
        pass

    return obj.__name__.lower()


def get_comping_short_help(obj: Any) -> str:
    """Returns the short help associated with process or action object.
    Defaults to a null-string."""
    try:
        return obj.__comping__.short_help
    except AttributeError:
        pass

    return ""


def get_comping_long_help(obj: Any) -> str:
    """Returns the long help associated with process or action object. Defaults to
    the docstring of the wrapped object, if available; otherwise a null string."""
    try:
        text = obj.__comping__.long_help
        if text:
            return text
    except AttributeError:
        pass

    try:
        return obj.__doc__
    except AttributeError:
        pass

    return ""


if __name__ == "__main__":

    @description(
        "person",
        short="This is decorator short help",
        long="This is decorator long help",
    )
    class Person1:
        def __init__(self, name: str) -> None:
            self.name = name

    print(get_comping_name(Person1))
    print(get_comping_short_help(Person1))
    print(get_comping_long_help(Person1))

    print()

    @description("person", short="This is decorator short help")
    class Person2:
        """This is doc string long help"""

        def __init__(self, name: str) -> None:
            self.name = name

    print(get_comping_name(Person2))
    print(get_comping_short_help(Person2))
    print(get_comping_long_help(Person2))
