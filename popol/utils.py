import os
import sys
from distutils.dir_util import copy_tree
from importlib import import_module
from typing import Any, Coroutine, TypeVar

from asyncer import syncify
from fastapi import FastAPI, HTTPException

T = TypeVar("T")
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


def get_settings(app: FastAPI, settings: T = None) -> T:
    """
    Get the settings from the application.

    Args:
        app: The application.
        settings: The settings.

    Raises:
        RuntimeError: If settings not found.

    Returns:
        Any: The settings.
    """

    if not hasattr(app, "state"):
        raise RuntimeError("The application does not have a state.")

    settings = getattr(app.state, "settings", settings)
    if not settings:
        raise RuntimeError("The application does not have a settings.")

    return settings


_current_app = None


def load_app() -> FastAPI:
    """
    Load the application.

    Returns:
        FastAPI: The application.
    """

    global _current_app

    if _current_app and isinstance(_current_app, FastAPI):
        return _current_app

    cwd = os.getcwd()
    sys.path.insert(0, cwd)
    env = os.getenv("POPOL_APP", "app.main:app")
    try:
        module, attr = env.rsplit(":", 1)
    except ValueError:
        raise RuntimeError("Invalid POPOL_APP environment variable.")

    try:
        _current_app = import_attr(f"{module}.{attr}")
    except ModuleNotFoundError:
        raise RuntimeError(
            f"Could not import {module} (make sure you are in the app's root directory)"
        )

    assert isinstance(_current_app, FastAPI)
    return _current_app


def abort(status_code: int, detail: Any = None, headers: dict = None):
    """
    Abort the request.

    Args:
        status_code: The status code.
        detail: The detail.
        headers: The headers.

    Raises:
        HTTPException: The HTTP exception.
    """

    raise HTTPException(status_code=status_code, detail=detail, headers=headers)


def run_sync(func: Coroutine, *args, **kwds):
    """
    Run async function to sync.

    Args:
        func: coroutine function
        \*args: argument to pass to func
        \*\*kwds: keyword argument to pass to func
    """

    return syncify(func)(*args, **kwds)
