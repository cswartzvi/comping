import abc
from dataclasses import dataclass, field
import inspect
from comping._typing import (
    Any,
    Annotated,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    runtime_checkable,
)

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


@dataclass(frozen=True)
class ActionProcressParameter:
    """Represnets a parameter from the initializer (__init__) or function call
    of an action or process object.

    Attributes:
        name: Name of the parameter (as it appears in the parameter).
        type_hint: Declared type hint of the parameter.
        params: An iterable of comping annotated parameters.
        default: The default value of the parameter. If supplied, must conform with
            declared type_hint.
    """

    name: str
    annotations: List[str] = field(default_factory=list)  # TODO: comping.Annotation
    type_hint: Optional[Type] = None
    default: Any = inspect.Parameter.empty  # None type is a valid default value

    def __post_init__(self):
        pass  # TODO: check that default (if defined) is compatible with type_type


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
        """Extract parameters from a process or process."""
        if not inspect.isclass(obj):
            return  # non-classes cannot have initialization parameters

        init = obj.__init__
        signature = inspect.signature(init)
        type_hints = get_type_hints(init, include_extras=True)

        for name, parameter in signature.parameters.items():
            if name in self._skip_parameters:
                continue

            type_hint = type_hints.get(name, None)
            annotations = []
            if get_origin(type_hint) is Annotated:
                # Note: According to PEP 560 annotated must have at least two arguments.
                type_hint, *annotations = get_args(type_hint)

            yield ActionProcressParameter(
                name=name,
                type_hint=type_hint,
                annotations=annotations,
                default=parameter.default,
            )
