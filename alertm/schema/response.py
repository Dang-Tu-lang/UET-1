from typing import List

from pydantic import BaseModel, Field


class MatchingAlert(BaseModel):
    alert_id: int = Field(
        ..., title="Alert ID", description="Alert ID matches event", ge=0
    )
    confidence: float = Field(
        ..., title="Confidence", description="Matching alert confidence"
    )


class AlertResp(BaseModel):
    message: str = Field(..., title="Message", description="Message")
    alerts: List[MatchingAlert] = Field(
        ..., title="Alerts", description="Alerts matching with event"
    )
