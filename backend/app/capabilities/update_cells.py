from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.google_sheets import GoogleSheetsClient


class UpdateCellsInput(BaseModel):
    spreadsheet_id: str
    range_a1: str
    values: List[List[Any]]


class UpdateCellsOutput(BaseModel):
    ok: bool = True
    cells_updated: int


class UpdateCells(Capability):
    name = "update_cells"
    Input = UpdateCellsInput
    Output = UpdateCellsOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = GoogleSheetsClient().update_cells(data.spreadsheet_id, data.range_a1, data.values)
        return UpdateCellsOutput(ok=True, cells_updated=res.get("cells_updated", 0)).model_dump()
