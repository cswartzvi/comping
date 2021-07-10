import abc
from typing import Callable, Iterable, Protocol, Type, TypeVar, Union

# from typing_extensions import Annotated


T_contra = TypeVar("T_contra", contravariant=True)


class SupportsAction(Protocol[T_contra]):
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
# 1. User defined classes that implement the SupportsAction protocol
# 2. Functions with call signatures similar to the SupportsAction protocol
T = TypeVar("T")
ActionTypeOrCallable = Union[Type[SupportsAction[T]], Callable[[T], bool]]


class Command:
    def __init__(
        self, process: Type[T], actions: Iterable[ActionTypeOrCallable[T]]
    ) -> None:
        self.process = process
        self.actions = actions
