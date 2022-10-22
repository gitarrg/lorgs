"""Lambda Entry Point."""

import mangum
from lorgs.app import create_app


app = create_app()
handler = mangum.Mangum(app)
