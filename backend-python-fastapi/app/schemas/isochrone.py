from __future__ import annotations

from datetime import date as DateType, time as TimeType
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class IsochroneQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_place: str = Field(..., alias="fromPlace", min_length=3)
    cutoff_sec: PositiveInt = Field(..., alias="cutoffSec")
    mode: str | None = Field(
        None,
        alias="mode",
        description="Comma separated OTP mode string (e.g. TRANSIT,WALK)",
    )
    date: DateType | None = Field(
        None,
        alias="date",
        description="Optional specific date in YYYY-MM-DD",
    )
    time: TimeType | None = Field(
        None,
        alias="time",
        description="Optional specific time in HH:MM format",
    )

    def to_query_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "fromPlace": self.from_place,
            "cutoffSec": str(self.cutoff_sec),
        }
        if self.mode:
            params["mode"] = self.mode
        if self.date:
            params["date"] = self.date.isoformat()
        if self.time:
            params["time"] = self.time.strftime("%H:%M")
        return params
