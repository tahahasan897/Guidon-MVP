from fastapi import APIRouter

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.get("/")
def list_runs():
    return [{"id": 1, "status": "completed", "goal": "demo"}]


@router.get("/{run_id}")
def get_run(run_id: int):
    return {"id": run_id, "status": "completed"}
