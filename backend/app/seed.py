from datetime import datetime, date
from app.db.session import SessionLocal
from app.db import models


def run():
    db = SessionLocal()
    try:
        # ensure org exists
        org = db.query(models.Org).first()
        if not org:
            org = models.Org(name="Demo Org")
            db.add(org)
            db.commit()
            db.refresh(org)
        # insert a sample metric
        if not db.query(models.MetricDaily).first():
            m = models.MetricDaily(
                org_id=org.id,
                date=datetime.utcnow(),
                mrr=10000,
                burn=5000,
                runway_months=6,
                mom_growth=0.05,
            )
            db.add(m)
            db.commit()
        print("Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
