from typing import List

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: int = Field(..., title="Event ID", description="Event ID")
    service: str = Field(..., title="Service", description="Service number")
    topic: str = Field(..., title="Topic", description="Topic name")
    environment: str = Field(
        ...,
        title="Environment",
        description="Environment name",
        examples=["production", "testing"],
    )
    content: str = Field(..., title="content", description="Event description")
    resource: str = Field(..., title="resource", description="Resource name")

class Alert(BaseModel):
    id: int = Field(..., title="Event ID", description="Event ID")
    service: str = Field(..., title="Service", description="Service number")
    topic: str = Field(..., title="Topic", description="Topic name")
    environment: str = Field(
        ...,
        title="Environment",
        description="Environment name",
        examples=["production", "testing"],
    )
    description: str = Field(..., title="Description", description="Alert description")
    resource: str = Field(..., title="resource", description="Resource name")


class MatchingRequest(BaseModel):
    event: Event = Field(..., title="Event", description="Event")
    alerts: List[Alert] = Field(..., title="Alerts", description="Alerts")
