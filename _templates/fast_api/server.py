from __future__ import annotations

import logging
import os
from http.client import HTTPException

from dotenv import load_dotenv
from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader

load_dotenv()
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Define Pydantic model for request body
X_API_KEY = APIKeyHeader(name="X_API_KEY")


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    """takes the X-API-Key header and validate it with the X-API-Key in the database/environment"""
    if x_api_key != os.environ["X_API_KEY"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key. Check that you are passing a 'X-API-Key' on your header.",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
