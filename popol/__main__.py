from typing import Optional

from pkg_resources import get_distribution
from popol.utils import copy_template_dir
from typer import Argument, Context, Option, Typer, echo, prompt

popol = Typer(
    name="popol", help="Popol CLI", no_args_is_help=True, invoke_without_command=True
)


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