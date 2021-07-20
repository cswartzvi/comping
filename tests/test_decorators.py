from comping.decorators import (
    description,
    get_comping_long_help,
    get_comping_name,
    get_comping_short_help,
)


def test_description_decorator_on_class():
    @description(name="name", short="Short help", long="Long help")
    class Testing:
        pass

    assert get_comping_name(Testing) == "name"
    assert get_comping_short_help(Testing) == "Short help"
    assert get_comping_long_help(Testing) == "Long help"


def test_description_decorator_on_function():
    @description(name="name", short="Short help", long="Long help")
    def function(process):
        pass

    assert get_comping_name(function) == "name"
    assert get_comping_short_help(function) == "Short help"
    assert get_comping_long_help(function) == "Long help"


def test_description_decorator_docstring_for_long_help():
    @description()
    def function(process):
        """Docstring long help."""
        pass

    assert get_comping_long_help(function) == "Docstring long help."


def test_description_decorator_docstring_override():
    @description(long="No I am the docstring")
    def function(process):
        """Docstring long help."""
        pass

    assert get_comping_long_help(function) == "No I am the docstring"


def test_retrive_from_non_decorated_class_without_docstring():
    class Testing:
        pass

    assert get_comping_name(Testing) == "testing"
    assert get_comping_short_help(Testing) == ""
    assert get_comping_long_help(Testing) == ""


def test_retrive_from_non_decorated_class_with_docstring():
    class Testing:
        """Docstring."""
        pass

    assert get_comping_name(Testing) == "testing"
    assert get_comping_short_help(Testing) == ""
    assert get_comping_long_help(Testing) == "Docstring."
