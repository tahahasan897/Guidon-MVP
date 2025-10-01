from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.metrics.engine import compute_metrics

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/latest")
def get_latest(db: Session = Depends(get_db)):
    item = (
        db.query(models.MetricDaily)
        .order_by(models.MetricDaily.date.desc())
        .first()
    )
    if item:
        return {
            "date": item.date,
            "mrr": item.mrr,
            "burn": item.burn,
            "runway_months": item.runway_months,
            "mom_growth": item.mom_growth,
        }
    # default stub
    return {
        "date": datetime.utcnow().date().isoformat(),
        "mrr": 0,
        "burn": 0,
        "runway_months": 0,
        "mom_growth": 0,
    }


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    items = (
        db.query(models.MetricDaily)
        .order_by(models.MetricDaily.date.asc())
        .all()
    )
    return [
        {
            "date": i.date,
            "mrr": i.mrr,
            "burn": i.burn,
            "runway_months": i.runway_months,
            "mom_growth": i.mom_growth,
        }
        for i in items
    ]


@router.post("/recompute")
def recompute(db: Session = Depends(get_db)):
    # Pull naive inputs from latest ingested events (placeholder)
    inputs = {"mrr": 10000, "burn": 5000, "cash": 30000, "mom_growth": 0.05}
    m = compute_metrics(inputs)
    row = models.MetricDaily(
        org_id=1,
        date=datetime.utcnow(),
        mrr=m["mrr"],
        burn=m["burn"],
        runway_months=m["runway_months"],
        mom_growth=m["mom_growth"],
    )
    db.add(row)
    db.commit()
    return {"ok": True}
