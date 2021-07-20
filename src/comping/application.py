import abc
import inspect

from comping._typing import (
    Any,
    Annotated,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Protocol,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    runtime_checkable,
)
from comping.annotations import is_annotation, is_valid_type_hint
from comping.parameters import ActionProcressParameter

T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Action(Protocol[T_contra]):
    """Defines the minimum contract for class based actions."""

    @abc.abstractmethod
    def __call__(self, process: T_contra) -> bool:
        """Executes action on a given process.

        Args:
            process: the process on which the action is executed.

        Returns:
            True if the action was successful, False otherwise.
        """
        ...


# Valid actions include:
# 1. User defined classes that implement the Action protocol
# 2. Functions with call signatures similar to the Action protocol
T = TypeVar("T")
ActionOrCallable = Union[Type[Action[T]], Callable[[T], bool]]


class ApplicationGroup:
    """Represents a group within a comping application.

    Args:
        process: The main process associated with the application group.
        actions: An iterable of actions that can be performed on the main process.
    """

    # TODO: expand docstring.

    _skip_parameters = {"self", "args", "kwargs"}

    def __init__(
        self, process: Type[T], actions: Iterable[ActionOrCallable[T]]
    ) -> None:
        self.process = process
        self.process_params = list(self._extract_params(self.process))

        self.actions_map: Dict[ActionOrCallable, List[ActionProcressParameter]] = {}
        for action in actions:
            self.actions_map[action] = list(self._extract_params(action))

    def _extract_params(self, obj: Any) -> Iterator[ActionProcressParameter]:
        """Yields extracted initialization parameters from a process or action.

        Args:
            obj: Represents any (potential) action or process.
        """
        if not inspect.isclass(obj):
            return  # non-classes cannot have initialization parameters

        init = obj.__init__
        signature = inspect.signature(init)
        type_hints = get_type_hints(init, include_extras=True)

        for name, parameter in signature.parameters.items():
            if name in self._skip_parameters:
                continue

            default = parameter.default
            type_hint = type_hints.get(name, None)
            type_args = get_args(type_hint)
            type_origin = get_origin(type_hint)

            annotations = []
            if type_origin is Annotated:
                # According to PEP 563 Annotated must have at least two arguments.
                type_hint, *annotations = type_args
                for annotation in annotations:
                    if not is_annotation(annotation):
                        raise ValueError(
                            f"Unknown annotation type '{parameter}' on '{obj}'"
                        )
                    if not is_valid_type_hint(type_hint, annotation):
                        raise ValueError(
                            f"Invalid type hint and annotation '{parameter}' on '{obj}'"
                        )
            elif type_origin is Union:
                # Currently, comping does not accept Union type hints with the major
                # expection of Union[T, NoneType] which is an aliased as Optional[T].
                # In this case if a parameter default was specified it must be None.
                if len(type_args) == 2 and type_args[1] is type(None):  # noqa: E721
                    if default != inspect.Parameter.empty and default is not None:
                        raise ValueError(
                            "Parameters declared as Optional must have default "
                            f"value of None: '{parameter}' on '{obj}'."
                        )
                    type_hint = type_args[0]
                else:
                    raise ValueError(
                        f"Union type hints are not allowed: '{parameter}' on '{obj}'"
                    )
            # TODO: screen for iterables

            if (
                type_hint is not None and
                parameter.default != inspect.Parameter.empty and
                not isinstance(default, type_hint)
            ):
                raise ValueError(
                    "Parameter defaults must be an instance of the declared "
                    f"type hint: '{parameter}' on '{obj}'"
                )

            yield ActionProcressParameter(
                name=name,
                type_hint=type_hint,
                annotations=annotations,
                default=parameter.default,
            )
