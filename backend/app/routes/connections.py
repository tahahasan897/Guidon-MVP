from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.connections import ConnectionCreate, ConnectionOut

router = APIRouter(prefix="/api/connections", tags=["connections"])


@router.get("/", response_model=list[ConnectionOut])
def list_connections(db: Session = Depends(get_db)):
    items = db.query(models.Connection).all()
    return [ConnectionOut.model_validate(i) for i in items]


@router.post("/", response_model=ConnectionOut)
def create_connection(payload: ConnectionCreate, db: Session = Depends(get_db)):
    # TODO: handle real OAuth state and token exchange
    conn = models.Connection(
        org_id=1,
        provider=payload.provider,
        status="connected",
        access_token_encrypted="",
        refresh_token_encrypted=None,
        expires_at=None,
    )
    db.add(conn)
    db.commit()
    db.refresh(conn)
    return ConnectionOut.model_validate(conn)


@router.delete("/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    conn = db.query(models.Connection).get(connection_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(conn)
    db.commit()
    return {"ok": True}
