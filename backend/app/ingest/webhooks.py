from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/hubspot")
async def hubspot_webhook(req: Request, db: Session = Depends(get_db)):
    payload = await req.json()
    evt = models.EventIngested(org_id=1, source="hubspot", payload=payload)
    db.add(evt)
    db.commit()
    return {"ok": True}


@router.post("/slack")
async def slack_webhook(req: Request, db: Session = Depends(get_db)):
    payload = await req.json()
    evt = models.EventIngested(org_id=1, source="slack", payload=payload)
    db.add(evt)
    db.commit()
    return {"ok": True}
