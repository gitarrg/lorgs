"""Define the Covanents Players can join."""

from lorgs.models.wow_covenant import WowCovenant


NO_COV = WowCovenant(id=0, name="None")
KYRIAN = WowCovenant(id=1, name="Kyrian")
VENTHYR = WowCovenant(id=2, name="Venthyr")
NIGHTFAE = WowCovenant(id=3, name="Nightfae")
NECROLORD = WowCovenant(id=4, name="Necrolord")
