from __future__ import annotations
from typing import Any, Dict, List
from pydantic import BaseModel
from app.capabilities.interface import Capability
from app.integrations.google_sheets import GoogleSheetsClient


class AppendRowsInput(BaseModel):
    spreadsheet_id: str
    range_a1: str
    rows: List[List[Any]]


class AppendRowsOutput(BaseModel):
    ok: bool = True
    rows_appended: int


class AppendRows(Capability):
    name = "append_rows"
    Input = AppendRowsInput
    Output = AppendRowsOutput

    def execute(self, org_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        data = self.Input(**params)
        res = GoogleSheetsClient().append_rows(data.spreadsheet_id, data.range_a1, data.rows)
        return AppendRowsOutput(ok=True, rows_appended=res.get("rows_appended", 0)).model_dump()
