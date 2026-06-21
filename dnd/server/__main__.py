import uvicorn  # type: ignore[import-not-found]
from dnd.server.app import app

if __name__ == "__main__":
    uvicorn.run(app)
