import sys
from typing import (  # noqa
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

if sys.version_info >= (3, 9):
    from typing import (  # noqa
        Annotated,
        Protocol,
        get_args,
        get_origin,
        get_type_hints,
        runtime_checkable,
    )
elif sys.version_info >= (3, 8):
    from typing import (  # noqa
        Protocol,
    )

    # Annotated not included in typing module before 3.9
    from typing_extensions import (  # noqa
        Annotated,
        get_args,
        get_origin,
        get_type_hints,
        runtime_checkable,
    )
else:
    # ...Protocol not included in typing module before 3.8
    from typing_extensions import (  # noqa
        Annotated,
        Protocol,
        get_args,
        get_origin,
        get_type_hints,
        runtime_checkable,
    )