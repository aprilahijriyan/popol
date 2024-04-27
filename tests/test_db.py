from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
from popol.db import sqlmodel
from popol.db.sqlmodel.globals import db

import pytest
from sqlmodel import select

from tests._models import Hero
from pydantic import BaseModel
from popol import dantic
from popol.utils import abort

from asgi_lifespan import LifespanManager


class HeroIn(BaseModel):
    name: str
    role: Hero.Roles

    def as_model(self):
        return Hero(**dantic.to_dict(self))

@pytest.fixture
def db_app(app: FastAPI):
    sqlmodel.setup(app)

    hero_router = APIRouter(prefix="/hero")
    
    @hero_router.get("/")
    async def list_hero():
        with db.open() as session:
            heroes = session.exec(select(Hero)).all()
            return heroes

    @hero_router.post("/")
    async def create_hero(hero_data: HeroIn):
        with db.open() as session:
            hero = hero_data.as_model()
            session.add(hero)
            session.commit()
            session.refresh(hero)
            return hero

    @hero_router.get("/{id}")
    async def get_hero(id: int):
        with db.open() as session:
            stmt = select(Hero).where(Hero.id == id)
            hero = session.exec(stmt).first()
            if not hero:
                abort(404, "Hero not found")
            return hero

    @hero_router.put("/{id}")
    async def update_hero(id: int, hero_data: HeroIn):
        with db.open() as session:
            stmt = select(Hero).where(Hero.id == id).with_for_update()
            hero = session.exec(stmt).first()
            if not hero:
                abort(404, "Hero not found")
            hero.name = hero_data.name
            hero.role = hero_data.role
            session.add(hero)
            session.commit()
            session.refresh(hero)
            return hero

    @hero_router.delete("/{id}")
    async def delete_hero(id: int):
        with db.open() as session:
            stmt = select(Hero).where(Hero.id == id)
            hero = session.exec(stmt).first()
            if not hero:
                abort(404, "Hero not found")
            session.delete(hero)
            session.commit()
            return {"detail": "Hero deleted"}

    app.include_router(hero_router)
    return app

@pytest.fixture
async def db_client(db_app: FastAPI):
    async with LifespanManager(db_app):
        with TestClient(db_app) as client:
            yield client

@pytest.mark.anyio
async def test_db_via_api(db_client: TestClient):
    # get all heroes
    resp = db_client.get("/hero/")
    all_heroes = resp.json()
    assert resp.status_code == 200 and len(all_heroes) == 0
    # create a hero
    resp = db_client.post("/hero/", json={"name": "Nana", "role": Hero.Roles.MIDLANE})
    created_hero = resp.json()
    assert resp.status_code == 200 and created_hero["name"] == "Nana" and created_hero["role"] == Hero.Roles.MIDLANE
    # get all heroes
    resp = db_client.get("/hero/")
    all_heroes = resp.json()
    assert resp.status_code == 200 and len(all_heroes) == 1
    # get a hero
    resp = db_client.get(f"/hero/{created_hero['id']}")
    hero = resp.json()
    assert resp.status_code == 200 and hero["name"] == "Nana" and hero["role"] == Hero.Roles.MIDLANE
    # update a hero
    resp = db_client.put(f"/hero/{created_hero['id']}", json={"name": "Nana", "role": Hero.Roles.JUNGLER})
    updated_hero = resp.json()
    assert resp.status_code == 200 and updated_hero["name"] == "Nana" and updated_hero["role"] == Hero.Roles.JUNGLER
    # get a hero
    resp = db_client.get(f"/hero/{created_hero['id']}")
    hero = resp.json()
    assert resp.status_code == 200 and hero["name"] == "Nana" and hero["role"] == Hero.Roles.JUNGLER
    # delete a hero
    resp = db_client.delete(f"/hero/{created_hero['id']}")
    assert resp.status_code == 200
    # get all heroes
    resp = db_client.get("/hero/")
    all_heroes = resp.json()
    assert resp.status_code == 200 and len(all_heroes) == 0
