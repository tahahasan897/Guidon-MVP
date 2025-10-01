from typing import Dict, Any, List


def detect_anomalies(metrics: Dict[str, Any]) -> List[str]:
    alerts: List[str] = []
    if metrics.get("burn", 0) > metrics.get("mrr", 0):
        alerts.append("Burn exceeds MRR")
    if metrics.get("mom_growth", 0) < -0.2:
        alerts.append("Revenue dropped >20% MoM")
    return alerts
