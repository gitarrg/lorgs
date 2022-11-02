

from pydantic import BaseModel

from .encounter import Encounter


class WorldData(BaseModel):
    """The world data object contains collections of data such as
    expansions, zones, encounters, regions, subregions, etc."""

    encounter: Encounter = Encounter()
    """Obtain a specific encounter by id."""
