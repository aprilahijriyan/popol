import os
from distutils.dir_util import copy_tree
from importlib import import_module
from typing import Any

POPOL_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def copy_template_dir(dest_dir: str, *, project_name: str, project_description: str):
    """
    Copy the template directory to the destination directory.

    Args:
        dest_dir (str): The destination directory.
        project_name (str): The project name.
        project_description (str): The project description.
    """

    dest_dir = os.path.abspath(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    copy_tree(POPOL_TEMPLATE_DIR, dest_dir)
    readme_path = os.path.join(dest_dir, "README.md")
    with open(readme_path, "r") as f:
        old_data = f.read()
        new_data = old_data.format(
            project_name=project_name, project_description=project_description
        )

    with open(readme_path, "w") as f:
        f.write(new_data)


def import_attr(module: str) -> Any:
    """
    Import attributes from a module.

    Args:
        module: Module name (e.g. "os.path")

    Returns:
        Any: Imported attributes
    """

    package, attr = module.rsplit(".", 1)
    mod = import_module(package)
    return getattr(mod, attr)
