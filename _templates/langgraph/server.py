from __future__ import annotations

import json
import logging
import os
import traceback
from http.client import HTTPException
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from config import parse_arguments, Config, create_config_with_args
from graph_builder import build_graph
from state import State
from utils.base_model_json_encoder import BaseModelJSONEncoder
from utils.filter_output_message import filter_output_messages

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


# Add a route to run the ai agent
@app.post("/generate", dependencies=[Depends(api_key_auth)])
async def generate_route(state: State):
    config = {"configurable": {"thread_id": "3"}}
    try:
        output = await graph.ainvoke(state, config)
        output["messages"] = filter_output_messages(output["messages"])
        logger.info(json.dumps(output["messages"], cls=BaseModelJSONEncoder))
        return {"success": True, "result": output}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stream", dependencies=[Depends(api_key_auth)])
async def stream(state: State):
    config = {"configurable": {"thread_id": "3"}}

    async def stream_generator(
        state: State, config: dict
    ) -> AsyncGenerator[str, None]:
        async for event in graph.astream_events(state, config, version="v2"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                yield json.dumps(
                    event["data"]["chunk"], cls=BaseModelJSONEncoder
                ) + "\n"
        output = event["data"]["output"]
        output["messages"] = filter_output_messages(output["messages"])
        logger.info(json.dumps(output["messages"], cls=BaseModelJSONEncoder))
        yield json.dumps(output, cls=BaseModelJSONEncoder)

    generator = stream_generator(state, config)
    try:
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    graph = build_graph(config)
    uvicorn.run(app, host="0.0.0.0", port=8080)
