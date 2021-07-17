from typing import Callable
from comping import Action, CommandGroup


class TestProcess:

    def __init__(self, name: str) -> None:
        self.name = name


class TestAction1:

    def __call__(self, process: TestProcess) -> bool:
        name = process.name
        print(f"Hello, {name} from {self.__class__.__name__}")
        return True


class TestAction2(Action[TestProcess]):
    def __call__(self, process: TestProcess) -> int:
        name = process.name
        print(f"Hello, {name} from {self.__class__.__name__}")
        return True


class TestAction3:
    def __call__(self, process: TestProcess) -> int:
        name = process.name
        print(f"Hello, {name} from {self.__class__.__name__}")
        return True


def test_action4(process: TestProcess) -> bool:
    name = process.name
    print(f"Hello, {name} from test_action4")
    return True


action: Callable[[TestProcess], bool] = TestAction1()


# cmd = CommandGroup(TestProcess, [TestAction1, TestAction2, TestAction3, test_action4])

group = CommandGroup(TestProcess, [TestAction1, test_action4])
print(group)