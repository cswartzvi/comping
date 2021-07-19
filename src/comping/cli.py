from dataclasses import dataclass, field
from inspect import Parameter

import click

from comping._typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    List,
    TypeVar,
)
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
    click_type = _get_click_type(parameter)
    if parameter.default == Parameter.empty:
        obj = click.argument(
            parameter.name,  #  TODO: Move to a function
            type=click_type
        )(obj)
    else:
        help = ""
        if parameter.annotations:
            help = parameter.annotations[0].help  #  TODO: Move to a function
        obj = click.option(
            f"--{parameter.name}",  #  TODO: Move to a function
            help=help,
            type=click_type,
            default=parameter.default
        )(obj)
    return obj


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
    for parameter in app.process_params:
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
    for parameter in parameters:
        command = _add_parameters(command, parameter)

    # Adds @parent.command(...)
    command = parent.command(
        name=get_comping_name(action),
        short_help=get_comping_short_help(action),
        help=get_comping_long_help(action),
    )(command)


def _get_click_type(parameter: ActionProcressParameter) -> Any:
    type_hint = parameter.type_hint
    if type_hint == str:
        return click.STRING
    elif type_hint == int:
        return click.INT
    elif type_hint == float:
        return click.FLOAT
    elif type_hint == bool:
        return click.BOOL
    else:
        return click.STRING
