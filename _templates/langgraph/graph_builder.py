import logging
import sys

from nodes.init import Init
from config import Config
from langgraph.graph.state import CompiledStateGraph
from state import State
from langgraph.graph import StateGraph
from langgraph.graph import END
from langgraph.graph import START

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def build_graph(config: Config) -> CompiledStateGraph:
    builder = StateGraph(State)
    builder.add_node("init", Init(config).execute)

    builder.add_edge(START, "init")
    builder.add_edge("init", END)

    return builder.compile()