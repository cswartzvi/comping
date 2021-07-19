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

    def gesture(self, motion: str) -> None:
        print(f"Gesture to {self.name}: {motion}")


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


@description("wave", "Gesture to the person.")
def wave(process: Person) -> bool:
    """Wave at the person."""
    process.gesture("Wave")
    return True


app = Application(Person, [Greet, wave])

cli = create_cli("testing", "Initial testing application", [app])

cli()
