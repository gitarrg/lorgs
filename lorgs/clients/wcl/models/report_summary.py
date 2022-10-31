# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, root_validator


class UnitInfo(BaseModel):
    name: str
    id: int
    guid: int
    type: str


class PlayerTotal(UnitInfo):
    """Per Player Name and Total."""
    total: int = 0


################################################################################


class DeathEventAbility(BaseModel):
    name: str = ""
    """Name of the Ability."""
    type: int = 0
    """DMG Type."""
    abilityIcon: str = ""


class DeathEvent(UnitInfo):
    """Event describing a players death."""
    deathTime: int
    ability: DeathEventAbility = DeathEventAbility(name="")


################################################################################


class CompositionEntrySpec(BaseModel):
    spec: str
    role: str


class CompositionEntry(UnitInfo):
    specs: list[CompositionEntrySpec]


################################################################################


class ReportSummary(BaseModel):

    totalTime: int
    itemLevel: float
    composition: list[CompositionEntry]
    damageDone: list[PlayerTotal]
    healingDone: list[PlayerTotal]

    deathEvents: list[DeathEvent]

    @root_validator(pre=True)
    def unwrap_data(cls, v):
        try:
            return v["data"]
        except KeyError:
            raise ValueError("Missing `data`.")
