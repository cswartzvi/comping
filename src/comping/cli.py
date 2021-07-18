from inspect import Parameter
from typing import Any, Callable, Iterable, List

import click

from comping.application import (
    ActionOrCallable,
    ActionProcressParameter,
    Application,
)
from comping.decorators import (
    get_comping_long_help,
    get_comping_name,
    get_comping_short_help,
)


def create_cli(name: str, help: str, apps: Iterable[Application]) -> Callable:
    @click.group(name=name, help=help)
    def cli():
        pass

    for app in apps:
        _create_cli_group(cli, app)

    return cli


def _add_parameters(obj: Any, parameter: ActionProcressParameter) -> click.Command:
    if parameter.default == Parameter.empty:
        obj = click.argument(
            parameter.name
        )(obj)
    else:
        help = ""
        if parameter.annotations:
            help = parameter.annotations[0]
        obj = click.option(
            f"--{parameter.name}",
            help=help,
            default=parameter.default
        )(obj)
    return obj


def _create_cli_group(parent: click.Group, app: Application) -> None:

    # Underlying click.group function to be associated with a comping process.
    # Note: all dynamic click decorators need to be added in REVERSE order.
    @click.pass_context
    def group(ctx, **kwargs):
        # TODO: parameter checking
        ctx.obj = app.process(**kwargs)

    # Adds @click.option(...) and @click.argument(...)
    for parameter in app.process_params:
        group = _add_parameters(group, parameter)

    # Adds @parent.group(...)
    group = parent.group(
        chain=True,
        name=get_comping_name(app.process),
        short_help=get_comping_short_help(app.process),
        help=get_comping_long_help(app.process),
    )(group)

    # Commands for actions are attached to this group
    for action, parameters in app.actions_map.items():
        _create_cli_command(group, action, parameters)


def _create_cli_command(
    parent: click.Group,
    action: ActionOrCallable,
    parameters: List[ActionProcressParameter],
) -> None:

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

    # Adds @click.option(...) and @click.argument(...)
    for parameter in parameters:
        command = _add_parameters(command, parameter)

    # Adds @parent.command(...)
    command = parent.command(
        name=get_comping_name(action),
        short_help=get_comping_short_help(action),
        help=get_comping_long_help(action),
    )(command)
