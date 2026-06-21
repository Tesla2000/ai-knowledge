from dnd.server.app import app
from mangum import Mangum

handler = Mangum(app)
