"""API-Routes to fetch Data about seasonal Data."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.data.seasons import ALL_SEASONS, CURRENT_SEASON


router = fastapi.APIRouter(tags=["seasons"], prefix="/seasons")


@router.get("/")
async def get_all_seasons() -> dict[str, list[str]]:
    return {"seasons": [season.name for season in ALL_SEASONS]}


@router.get("/current")
async def get_current_seasons() -> str:
    return CURRENT_SEASON.name
