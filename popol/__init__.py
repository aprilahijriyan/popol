"""
Popol is a library that provides as-is tools for use on FastAPI.
These are the features currently available:

* Caching - Provides a simple API for saving results to a temporary database.
* ORM Integration
    * SQLModel - Provides a plugin to seamlessly integrate SQLModel with FastAPI.
* Email - Provides a simple API for sending emails.
* Background Jobs:
    * SAQ - SAQ queue integration support for task scheduling.
* Pagination

"""

try:
    import fastapi  # noqa
    import pydantic  # noqa
except ModuleNotFoundError:
    raise RuntimeError(
        "Some modules are missing. Run the command below to install the module. ``pip install fastapi pydantic``"
    )
