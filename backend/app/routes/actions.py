from fastapi import APIRouter

router = APIRouter(prefix="/api/actions", tags=["actions"])


@router.get("/by_run/{run_id}")
def list_actions_by_run(run_id: int):
    return [{"id": 1, "run_id": run_id, "status": "success"}]


@router.get("/{action_id}")
def get_action(action_id: int):
    return {"id": action_id, "status": "success"}
