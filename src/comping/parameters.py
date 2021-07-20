from dataclasses import dataclass, field
import inspect

from comping._typing import Any, List, Optional, Type
from comping.annotations import Annotation


@dataclass(frozen=True)
class ActionProcressParameter:
    """Represnets a parameter from the initializer of an action or process object.

    Attributes:
        name: Name of the parameter (as it appears in the parameter).
        type_hint: Declared type hint of the parameter.
        params: An iterable of comping annotated parameters.
        default: The default value of the parameter. If supplied, must conform with
            declared type_hint.
    """

    name: str
    annotations: List[Annotation] = field(default_factory=list)
    type_hint: Optional[Type] = None
    default: Any = inspect.Parameter.empty  # None type is a valid default value
