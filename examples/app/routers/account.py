from fastapi import APIRouter, Request
from popol.cache.decorators import cached
from popol.db.sqlmodel import Database
from popol.utils import abort
from pydantic import BaseModel
from sqlalchemy import desc

from app.core.pagination import get_paginated_response
from app.models import Account


class AccountCreate(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/", summary="Get all accounts")
@cached(cache="aioredis")
def get_accounts(request: Request, page: int = 1, page_size: int = 10):
    """
    Get all accounts.
    """

    db: Database = request.app.state.db
    with db.open() as session:
        data = session.query(Account).order_by(desc(Account.id))
        return get_paginated_response(data, page, page_size)


@router.post("/", summary="Create a new account")
async def create_account(request: Request, body: AccountCreate):
    """
    Create a new account.
    """

    db: Database = request.app.state.db
    with db.open() as session:
        account = Account(**body.dict())
        session.add(account)
        session.commit()
        session.refresh(account)
        return account.dict()


@router.get("/{id}", summary="Get an account")
async def get_account(request: Request, id: int):
    """
    Get an account.
    """

    db: Database = request.app.state.db
    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        return account.dict()


@router.put("/{id}", summary="Update an account")
async def update_account(request: Request, id: int, body: AccountCreate):
    """
    Update an account.
    """

    db: Database = request.app.state.db
    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        account.username = body.username
        account.password = body.password
        session.add(account)
        session.commit()
        session.refresh(account)
        return account.dict()


@router.delete("/{id}", summary="Delete an account")
async def delete_account(request: Request, id: int):
    """
    Delete an account.
    """

    db: Database = request.app.state.db
    with db.open() as session:
        account: Account = session.query(Account).where(Account.id == id).first()
        if not account:
            abort(404, "Account not found")

        session.delete(account)
        session.commit()
        return {"detail": "Account deleted"}
