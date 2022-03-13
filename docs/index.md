# Popol ⛅

> Third party packages for your FastAPI projects ⛅

Popol is a library that provides as-is tools for use on FastAPI.

This project aims to provide APIs to support your FastAPI projects without breaking existing projects. This is another version of the [Fastack](https://github.com/fastack-dev/fastack) project. Overall the available APIs are not much different from the [Fastack plugins](https://github.com/fastack-dev).

## Features 🌟

- [x] Project Layout
- [x] Command Line Interface (like `flask` command)
- [x] Pagination
- Cache Framework

    - Backends

        - [x] Redis
        - [x] Aioredis
        - [ ] Memcached

    - Serializers

        - [x] JSON
        - [x] Pickle
        - [ ] MsgPack

- ORM Integration

    - [x] SQLModel (Async/Sync)
    - [ ] Tortoise ORM

- ODM Integration

    - [ ] MongoEngine

- [x] SMTP client (using aioredis) to send emails.
- Background Jobs:

    - [x] SAQ queue support for task scheduling


## Installation 📚

```
pip install popol
```
