from typing_extensions import Annotated

from comping import Application, description
from comping.cli import create_cli


@description("person", "Interactions with a person")
class Person:
    """Constructs a person using the specified NAME."""

    def __init__(self, name: str) -> None:
        self.name = name

    def talk(self, text: str) -> None:
        print(text)


@description("greet", "Greet a person.")
class Greet:
    """Generate a greeting using a specified PHRASE."""

    def __init__(
        self, phrase: str, punctuation: Annotated[str, "Optional punctuation."] = "."
    ) -> None:
        self.phrase = phrase
        self.punctuation = punctuation

    def __call__(self, process: Person) -> bool:
        text = f"{self.phrase.title()}, {process.name.title()}{self.punctuation}"
        process.talk(text)
        return True


app = Application(Person, [Greet])

cli = create_cli("testing", "Initial testing application", [app])

cli()
