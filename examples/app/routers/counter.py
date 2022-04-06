from fastapi import APIRouter, Request
from popol.db.sqlmodel import Database

from app.models import Counter

router = APIRouter(prefix="/counter", tags=["Counter"])


@router.get("/", summary="Get the current value of the counter")
async def get_counter(request: Request):
    """
    Get the current value of the counter
    """
    db: Database = request.app.state.db
    with db.open() as session:
        counter = session.query(Counter).first()
        if counter is None:
            counter = Counter(value=0)
            session.add(counter)
            session.commit()
        return {"value": counter.value}
