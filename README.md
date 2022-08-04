# Popol ⛅

> Adding new power to your FastAPI application ⛅

Popol is a library that provides as-is tools for use on FastAPI.

This project aims to provide APIs to support your FastAPI projects without breaking existing projects. This is another version of the [Fastack](https://github.com/fastack-dev/fastack) project. Overall the available APIs are not much different from the [Fastack plugins](https://github.com/fastack-dev).

## Features 🌟

- [x] Project Layout
- [x] Command Line Interface (like `flask` command)
- [x] Pagination
- Cache Framework

    - Backends

        - [x] Redis (Sync/Async)
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

- [x] SMTP client (using aiosmtplib) to send emails.
- Background Jobs:

    - [x] SAQ queue support for task scheduling


## Installation 📚

```
pip install popol>=0.4.0
```

## Documentation 📖

Not available at this time, please learn from the [examples](https://github.com/aprilahijriyan/popol/tree/main/examples).
