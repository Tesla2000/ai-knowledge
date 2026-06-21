from dnd.server.app import app
from mangum import Mangum  # type: ignore[import-not-found]

handler = Mangum(app)
