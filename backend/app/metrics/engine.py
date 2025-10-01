from datetime import date
from typing import Dict, Any


def compute_metrics(inputs: Dict[str, Any]) -> Dict[str, Any]:
    mrr = float(inputs.get("mrr", 0))
    burn = float(inputs.get("burn", 0))
    runway_months = (inputs.get("cash", 0) / burn) if burn > 0 else 0
    mom_growth = float(inputs.get("mom_growth", 0))
    return {
        "date": date.today().isoformat(),
        "mrr": mrr,
        "burn": burn,
        "runway_months": runway_months,
        "mom_growth": mom_growth,
    }
