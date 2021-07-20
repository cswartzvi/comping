from dataclasses import dataclass, field
from inspect import Parameter
import inspect

import click

from comping._typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    TypeVar,
)
from comping.annotations import ParameterType, PriorityAnnotation, StandardAnnotation
from comping.application import (
    ActionOrCallable,
    ActionProcressParameter,
    ApplicationGroup,
)
from comping.decorators import (
    get_comping_long_help,
    get_comping_name,
    get_comping_short_help,
)

T = TypeVar("T")


@dataclass
class Context(Generic[T]):
    process: T
    actions: List[ActionOrCallable[T]] = field(default_factory=list)


def create_cli(name: str, help: str, apps: Iterable[ApplicationGroup]) -> click.Group:
    """Creates a comping command line interface.

    Args:
        name: Name high-level command line application.
        help (str): Help text for high-level command line application.
        app_groups: An iterable of comping application groups.


    """
    @click.group(name=name, help=help)
    def cli():
        pass

    for app in apps:
        _create_click_sub_group(cli, app)

    return cli


def _add_parameters(obj: Callable, parameter: ActionProcressParameter) -> Callable:
    """Adds parameters (arguments and options) to a click command or group.

    Args:
        obj: The specified 'click' command or group.
        parameter: The parameter to be added to the specified command or group.

    Returns:
        Callable: A click command or group with updated parameters.
    """
    kwargs: Dict[str, Any] = {"type": parameter.type_hint}  # TODO: handle iterable types

    if parameter.default == Parameter.empty:
        args = [parameter.name]

        param_type = ParameterType.ARGUMENT
    else:
        args = [f"--{parameter.name}"]
        param_type = ParameterType.OPTION
        if parameter.default != inspect.Parameter.empty:
            kwargs['default'] = parameter.default
            kwargs['show_default'] = True

    for annotation_type in [PriorityAnnotation, StandardAnnotation]:
        for annotation in parameter.annotations:
            if isinstance(annotation, annotation_type):
                name = parameter.name
                type_hint = parameter.type_hint
                default = parameter.default

                new_args = annotation.args(name, type_hint, default, param_type)
                args = new_args if new_args else args

                new_kwargs = annotation.kwargs(name, type_hint, default, param_type)
                kwargs.update(new_kwargs)

    if param_type == ParameterType.ARGUMENT:
        return click.argument(*args, **kwargs)(obj)
    else:
        return click.option(*args, **kwargs)(obj)


def _create_click_sub_group(parent: click.Group, app: ApplicationGroup) -> None:
    """Creates a 'click' sub-group for a comping application and attaches relevant actions.

    Args:
        parent: Parent of the sub-group (sub-group will a nested click.Group).
        app: Comping application defining the process and actions.
    """

    # Underlying click.group function to be associated with a comping process.
    # Note: all dynamic click decorators need to be added in REVERSE order.
    @click.pass_context
    def sub_group(ctx, **kwargs):
        # TODO: parameter checking
        ctx.obj = app.process(**kwargs)

    # Adds @click.option(...) and/or @click.argument(...)
    for parameter in reversed(app.process_params):
        sub_group = _add_parameters(sub_group, parameter)

    # Adds @parent.group(...)
    sub_group = parent.group(
        chain=True,
        name=get_comping_name(app.process),
        short_help=get_comping_short_help(app.process),
        help=get_comping_long_help(app.process),
    )(sub_group)

    # Commands for actions are attached to this group
    for action, parameters in app.actions_map.items():
        _create_click_command(sub_group, action, parameters)


def _create_click_command(
    parent: click.Group,
    action: ActionOrCallable,
    parameters: List[ActionProcressParameter],
) -> None:
    """Creates a 'click' command for a single comping action.

    Args:
        parent: Parent of the command.
        action: Individual comping action.
        parameters: Comping action associated with the specified action
    """

    # Underlying click.command function to be associated with a comping action.
    # Note: all dynamic click decorators need to be added in REVERSE order.
    @click.pass_obj
    def command(process, **kwargs):
        # TODO: restriction checking
        if not parameters:
            action(process)
            return
        # TODO: parameter checking
        instance = action(**kwargs)
        instance(process)

    # Adds @click.option(...) and/or @click.argument(...)
    for parameter in reversed(parameters):
        command = _add_parameters(command, parameter)

    # Adds @parent.command(...)
    command = parent.command(
        name=get_comping_name(action),
        short_help=get_comping_short_help(action),
        help=get_comping_long_help(action),
    )(command)
