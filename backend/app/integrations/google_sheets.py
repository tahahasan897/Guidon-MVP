from typing import List, Dict, Any

class GoogleSheetsClient:
    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def append_rows(self, spreadsheet_id: str, range_a1: str, rows: List[List[Any]]) -> Dict[str, Any]:
        return {"spreadsheet_id": spreadsheet_id, "range": range_a1, "rows_appended": len(rows)}

    def update_cells(self, spreadsheet_id: str, range_a1: str, values: List[List[Any]]) -> Dict[str, Any]:
        return {"spreadsheet_id": spreadsheet_id, "range": range_a1, "cells_updated": sum(len(r) for r in values)}
