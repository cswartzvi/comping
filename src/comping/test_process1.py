import click

from comping import ApplicationGroup, description
from comping.decorators import (
    get_comping_long_help,
    get_comping_name,
    get_comping_short_help,
)


@description("person", "Short help for person")
class Person:
    """Long help for Person."""

    def __init__(self, name: str) -> None:
        self.name = name

    def talk(self, text: str) -> None:
        print(text)


@description("greet", "Short help for greetings.")
class Greet:
    """Long help for Greet."""

    def __init__(self, phrase: str) -> None:
        self.phrase = phrase

    def __call__(self, process: Person) -> bool:
        text = f"{self.phrase.title()}, {process.name.title()}!"
        process.talk(text)
        return True


app = ApplicationGroup(Person, [Greet])


@click.group()
def cli():
    """Test automation tool"""
    pass


@cli.group(
    chain=True,
    name=get_comping_name(Person),
    short_help=get_comping_short_help(Person),
    help=get_comping_long_help(Person)
)
@click.argument("name", type=str)
@click.pass_context
def subgroup(ctx, **kwargs):
    ctx.obj = app.process(**kwargs)


@subgroup.command(
    name=get_comping_name(Greet),
    short_help=get_comping_short_help(Greet),
    help=get_comping_long_help(Greet)
)
@click.argument("phrase", type=str)
@click.pass_obj
def command(person, **kwargs):
    action = Greet(**kwargs)
    action(person)


cli()
