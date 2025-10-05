# backend/app/jobs/hello.py
from time import sleep
from app.db.session import SessionLocal
from app.db.models import AgentRun

def hello_world(run_id: int, name: str = "world"):
    # pretend work
    sleep(2)
    msg = f"hello, {name}!"
    # persist result
    with SessionLocal() as db:
        run = db.get(AgentRun, run_id)
        run.status = "completed"
        run.output = msg  # Store the message in the output field
        db.commit()
    return msg