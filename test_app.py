import click


class Application:

    def __init__(self, exe):
        self.exe = exe


@click.group()
def automate():
    "QUANTICS automation tool"
    pass


@automate.group(chain=True, short_help="Naval Munitions Requirement Process")
@click.option("--exe", help="the path to the executable.")
@click.pass_context
def nmrp(ctx, exe):
    """Long help for NMRPSS model runs."""
    ctx.obj = Application(exe)


@nmrp.command(short_help="Shield only model run")
@click.argument("trials", type=int)
@click.option("--iter1", type=bool, is_flag=True, help="First iteration only", default=False)
@click.pass_obj
def shield(app, trials, iter1):
    """"Long help for the shield only model run."""
    print(F"Running shield from {app.exe} with {trials=} {iter1=}")


@nmrp.command(short_help="NMRPSS full model run")
@click.argument("trials", type=int)
@click.option("--iter1", type=bool, is_flag=True, help="First iteration only", default=False)
@click.pass_obj
def full(app, trials, iter1):
    """"Long help for the full NMRPSS model run."""
    print(f"Running full NMRPSS from {app.exe} with {trials=} {iter1=}")


@automate.group(chain=True, short_help="JWS")
@click.option("--exe", help="the path to the executable.")
@click.pass_context
def jws(ctx, exe):
    """Long help for JWS."""
    ctx.obj = Application(exe)


@jws.command(short_help="Compute scenario files")
@click.argument("source", type=str)
@click.argument("destinaton", type=str)
@click.pass_obj
def compute(app, source, destinaton):
    """Long help for JWS compute."""
    print(F"Running compute from {app.exe} with {source=} {destinaton=}")


automate()
