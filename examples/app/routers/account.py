from fastapi import APIRouter, Request
from popol.cache.decorators import cached
from popol.db.sqlmodel.globals import db
from popol.schema import Page
from popol.utils import abort
from popol import dantic
from pydantic import BaseModel
from sqlalchemy import desc

from app.core.pagination import get_paginated_response
from app.models import Account
from app.schema import DetailSchema


class AccountCreate(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/", summary="Get all accounts", response_model=Page[Account])
@cached(cache="aioredis")
def get_accounts(request: Request, page: int = 1, page_size: int = 10):
    """
    Get all accounts.
    """

    with db.open() as session:
        data = session.query(Account).order_by(desc(Account.id))
        return get_paginated_response(data, page, page_size)


@router.post("/", summary="Create a new account", response_model=Account)
async def create_account(request: Request, body: AccountCreate):
    """
    Create a new account.
    """

    with db.open() as session:
        account = Account(**dantic.to_dict(body))
        session.add(account)
        session.commit()
        session.refresh(account)
        return dantic.to_dict(account)


@router.get("/{id}", summary="Get an account", response_model=Account)
async def get_account(request: Request, id: int):
    """
    Get an account.
    """

    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        return dantic.to_dict(account)


@router.put("/{id}", summary="Update an account", response_model=Account)
async def update_account(request: Request, id: int, body: AccountCreate):
    """
    Update an account.
    """

    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        account.username = body.username
        account.password = body.password
        session.add(account)
        session.commit()
        session.refresh(account)
        return dantic.to_dict(account)


@router.delete("/{id}", summary="Delete an account", response_model=DetailSchema)
async def delete_account(request: Request, id: int):
    """
    Delete an account.
    """

    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        session.delete(account)
        session.commit()
        return {"detail": "Account deleted"}
