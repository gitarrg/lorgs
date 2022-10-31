# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel


class User(BaseModel):
    """A single user of the site."""

    id: int = 0
    """The ID of the user."""

    name: str = ""
    """The name of the user."""
