from pydantic import BaseModel, Field


class UserDeviceInformation(BaseModel):
    application_id: str = Field(..., title="Application ID")
    device_id: str = Field(..., title="Device ID")
    device_kind: str = Field(..., title="Device Type")


class PeopleInteractionBehaviour(BaseModel):
    online_each_day: str = Field(..., title="Online Perday")
    time_per_day: str = Field(..., title="Time per day")
    location: str = Field(..., title="Location")

