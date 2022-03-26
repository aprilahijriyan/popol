import os
from typing import Optional

from pkg_resources import get_distribution, iter_entry_points
from typer import Argument, Context, Option, Typer, echo, prompt

from popol.utils import copy_template_dir

popol = Typer(
    name="popol", help="Popol CLI", no_args_is_help=True, invoke_without_command=True
)


def load_commands():
    """
    Load all global commands from entry point to `popol` command.
    """
    for ep in iter_entry_points("popol.commands"):
        try:
            cmd = ep.load()
            if isinstance(cmd, Typer):
                popol.add_typer(cmd)
            else:
                popol.command(ep.name, cmd)
        except Exception:
            # TODO: log error
            pass


@popol.callback()
def init(
    ctx: Context,
    version: Optional[bool] = Option(
        None, "-v", "--version", is_eager=True, help="Show version number and exit"
    ),
):
    if ctx.resilient_parsing:  # pragma: no cover
        return

    if version:
        ver = get_distribution("popol").version
        echo(f"popol v{ver}")
        ctx.exit()


@popol.command("init")
def init(outdir: str = Argument(None, help="The output directory")):
    """
    Initialize a new Popol project.
    """

    if outdir is None:
        echo("Please specify an output directory.", err=True)
        exit(1)

    project_name: str = prompt("Project name (e.g. Powerful API): ")
    project_description: str = prompt("Project description (e.g. A powerful API): ")
    echo("Initialize a new Popol project...")
    copy_template_dir(
        outdir, project_name=project_name, project_description=project_description
    )
    echo("Your project has been created in {}".format(outdir))


if "POPOL_COMMAND_INITIALIZED" not in os.environ:
    load_commands()
    os.environ["POPOL_COMMAND_INITIALIZED"] = "1"
