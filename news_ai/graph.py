from news_ai.schema import State
from news_ai.nodes import orchestrator, synthesizer, llm_call, assign_workers, news_ai
from langgraph.graph import StateGraph, START, END

def synth_mind():
    # Build workflow
    builder = StateGraph(State)

    # Add the nodes
    builder.add_node("news_ai", news_ai)
    # builder.add_node("verify_news", verify_news)
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("llm_call", llm_call)
    builder.add_node("synthesizer", synthesizer)

    # Add edges to connect nodes
    builder.add_edge(START, "news_ai")
    builder.add_edge("news_ai", "orchestrator")
    # builder.add_edge("news_ai", "verify_news")
    # builder.add_edge("verify_news", "orchestrator")
    builder.add_conditional_edges(
        "orchestrator", assign_workers, ["llm_call"]
    )
    builder.add_edge("llm_call", "synthesizer")
    builder.add_edge("synthesizer", END)

    # Compile the workflow
    graph = builder.compile()

    return graph


def explainer():
    # Build workflow
    builder = StateGraph(ExplainerState)

    # Add the nodes
    builder.add_node("explainer", explainer)

    # Add edges to connect nodes
    builder.add_edge(START, "explainer")
    builder.add_edge("explainer", END)

    # Compile the workflow
    graph_2 = builder.compile()

    return graph_2







