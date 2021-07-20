import abc
import enum
import pathlib

import click

from comping._typing import Any, Dict, List


class ParameterType(enum.Enum):
    ARGUMENT = 1
    OPTION = 2


class Annotation(abc.ABC):
    def args(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> List[str]:
        return list()

    def kwargs(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> Dict[str, Any]:
        return dict()

    @abc.abstractmethod
    def validate_type_hint(self, type_hint: Any) -> bool:
        ...


class PriorityAnnotation(Annotation):
    pass


class Help(PriorityAnnotation):
    def __init__(self, text: str) -> None:
        self.text = text

    def kwargs(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> Dict[str, Any]:
        if param_type == ParameterType.OPTION:
            return {"help": self.text}
        return dict()  # click arguments have no help

    def validate_type_hint(self, type_hint: Any) -> bool:
        return True  # Valid for any type hint


class Name(PriorityAnnotation):
    def __init__(self, text: str) -> None:
        self.text = text

    def args(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> List[str]:
        if param_type == ParameterType.ARGUMENT:
            return [name]
        else:
            return [f"--{self.text}", name]

    def kwargs(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> Dict[str, Any]:
        if param_type == ParameterType.ARGUMENT:
            return {"metavar": self.text}
        return dict()  # click options use args for name

    def validate_type_hint(self, type_hint: Any) -> bool:
        return True  # Valid for any type hint


class StandardAnnotation(Annotation):
    pass


class Path(StandardAnnotation):
    def __init__(
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        readable: bool = True,
        writeable: bool = False,
        resolve_path: bool = False,
        allow_dash: bool = False,
    ) -> None:
        self.exists = exists
        self.file_okay = file_okay
        self.dir_okay = dir_okay
        self.readable = readable
        self.writeable = writeable
        self.resolve_path = resolve_path
        self.allow_dash = allow_dash

    def validate_type_hint(self, type_hint: Any) -> bool:
        return type_hint in {pathlib.Path, str}

    def kwargs(
        self, name: str, type_hint: Any, default: Any, param_type: ParameterType
    ) -> Dict[str, Any]:
        path_type = click.Path(
            exists=self.exists,
            file_okay=self.file_okay,
            dir_okay=self.dir_okay,
            readable=self.readable,
            writable=self.writeable,
            resolve_path=self.resolve_path,
            allow_dash=self.allow_dash,
            path_type=type_hint
        )
        return {"type": path_type}


class Directory(Path):
    def __init__(
        self,
        exists: bool = False,
        readable: bool = True,
        writeable: bool = False,
        resolve_path: bool = False,
        allow_dash: bool = False,
    ) -> None:
        super().__init__(
            exists=exists,
            file_okay=False,
            dir_okay=True,
            readable=readable,
            writeable=writeable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
        )


class File(Path):
    def __init__(
        self,
        exists: bool = False,
        readable: bool = True,
        writeable: bool = False,
        resolve_path: bool = False,
        allow_dash: bool = False,
    ) -> None:
        super().__init__(
            exists=exists,
            file_okay=True,
            dir_okay=False,
            readable=readable,
            writeable=writeable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
        )


def is_annotation(obj: Any) -> bool:
    """Returns True if an object is a valid comping annotation; otherwise False."""
    return isinstance(obj, Annotation)


def is_valid_type_hint(type_hint: Any, annotation: Annotation) -> bool:
    """Returns True is the specified type hint and annonation combination is valid."""
    return annotation.validate_type_hint(type_hint)
