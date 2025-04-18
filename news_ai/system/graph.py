from news_ai.structure.schema import State, ExplainerState
from news_ai.agents.nodes import orchestrator, synthesizer, llm_call, assign_workers, news_ai, explainer
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


def help_search():
    # Build workflow
    builder_2 = StateGraph(ExplainerState)

    # Add the nodes
    builder_2.add_node("explainer", explainer)

    # Add edges to connect nodes
    builder_2.add_edge(START, "explainer")
    builder_2.add_edge("explainer", END)

    # Compile the workflow
    graph_2 = builder_2.compile()

    return graph_2


news = synth_mind()




