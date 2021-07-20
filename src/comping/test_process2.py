import pathlib
from typing import Optional
from typing_extensions import Annotated

from comping import ApplicationGroup, description
from comping.annotations import Help, Name, File, Directory
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
        self,
        phrase: str,
        directory: Annotated[pathlib.Path, Name("DIR"), Directory(exists=True)],
        punctuation: str = "!"
    ) -> None:
        self.phrase = phrase
        self.punctuation = punctuation
        self.directory = directory
        self.directory.mkdir(exist_ok=True, parents=True)
        print(type(self.directory))

    def __call__(self, process: Person) -> bool:
        text = f"{self.phrase.title()}, {process.name.title()}{self.punctuation}"
        process.talk(text)
        return True


@description("wave", "Gesture to the person.")
def wave(process: Person) -> bool:
    """Wave at the person."""
    process.gesture("Wave")
    return True


app = ApplicationGroup(Person, [Greet, wave])

cli = create_cli("testing", "Initial testing application", [app])

cli()
