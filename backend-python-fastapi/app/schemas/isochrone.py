from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class TransportMode(str, Enum):
    """이동 수단"""
    WALK = "WALK"
    TRANSIT = "TRANSIT"
    BICYCLE = "BICYCLE"
    CAR = "CAR"


class IsochroneQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="출발 위도 (latitude)",
    )
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="출발 경도 (longitude)",
    )
    cutoff_min: PositiveInt = Field(
        ...,
        alias="cutoffMin",
        description="최대 이동 시간 (분 단위)",
    )
    modes: list[TransportMode] | None = Field(
        default=[TransportMode.WALK, TransportMode.TRANSIT],
        description="이동 수단 목록",
    )
    arrive_by: bool = Field(
        False,
        alias="arriveBy",
        description="도착 시간 기준 여부 (False: 출발 시간 기준)",
    )

    def to_query_params(self) -> dict[str, Any]:
        # Convert lat/lon to location
        params: dict[str, Any] = {
            "location": f"{self.lat},{self.lon}",
        }

        # Convert cutoff_min to ISO-8601 duration format (PT{minutes}M)
        params["cutoff"] = f"PT{self.cutoff_min}M"

        # Use current time in ISO-8601 format with timezone
        now = datetime.now(timezone.utc).astimezone()
        params["time"] = now.isoformat()

        # modes parameter (plural) - convert enum list to comma-separated string
        if self.modes:
            params["modes"] = ",".join(mode.value for mode in self.modes)

        # arriveBy parameter
        params["arriveBy"] = str(self.arrive_by).lower()

        return params
