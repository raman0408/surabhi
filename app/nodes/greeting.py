from app.graph.stages import (
    IDENTITY
)

from app.services.language import (
    get_text
)


def greeting_node(state):

    return {
        **state,
        "current_stage": IDENTITY,
        "response": get_text(
            state,
            "greeting_intro"
        )
    }