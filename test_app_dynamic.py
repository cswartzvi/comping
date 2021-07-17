import click


class Application:

    def __init__(self, exe):
        self.exe = exe


def create_cli():

    @click.group()
    def cli():
        "QUANTICS automation tool"
        pass


def create_sub_group():
    
