from langgraph.graph import StateGraph
from langgraph.graph import END

from app.graph.state import SurabhiState

from app.nodes.greeting import greeting_node
from app.nodes.identity import identity_node
from app.nodes.identity_confirmation import identity_confirmation_node
from app.graph.stages import (
    GREETING,
    IDENTITY,
    IDENTITY_CONFIRMATION
)

def build_graph():
    graph = StateGraph(SurabhiState)

    graph.add_node(
        GREETING,
        greeting_node
    )

    graph.add_node(
        IDENTITY,
        identity_node
    )
    
    graph.add_node(
        IDENTITY_CONFIRMATION,
        identity_confirmation_node
    )

    graph.set_entry_point(GREETING)

    graph.add_edge(
        GREETING,
        IDENTITY
    )

    graph.add_conditional_edges(
        IDENTITY,
        identity_router,
        {
            IDENTITY: IDENTITY,
            IDENTITY_CONFIRMATION: IDENTITY_CONFIRMATION
        }
    )

    graph.add_edge(
        IDENTITY_CONFIRMATION,
        END
    )

    return graph.compile()




def identity_router(state):
    if state["current_stage"] == IDENTITY_CONFIRMATION:
        return IDENTITY_CONFIRMATION
    
    return IDENTITY