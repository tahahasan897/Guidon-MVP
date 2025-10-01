from typing import Dict, Any


def normalize_hubspot_contact(contact: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source": "hubspot",
        "email": contact.get("email"),
    }


def normalize_quickbooks_revenue(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {"source": "quickbooks", "mrr": snapshot.get("mrr", 0)}
