from fastapi import Request, HTTPException
from .database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def retrieve_token(request: Request):
    token = request.headers.get("token")
    if token is None:
        raise HTTPException(400, "no token header")
    
    request.state.token = token
    return token