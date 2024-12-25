from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_groq import ChatGroq
from IPython.display import display, Image

class State(TypedDict):
    query: str
    category: str
    sentiment: str
    response: str

from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

def categorize(state: State) -> State:
    "Technical, Billing, General"
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following query into one of these categories: "
        "Technical, Billing, General. Query: {query}"
    )
    chain = prompt | llm
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def analyze_sentiment(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Analyze the sentiment of the following customer query. "
        "Response with either 'Positive', 'Neutral', 'Negative'. Query: {query}"
    )
    chain = prompt | llm
    sentiment = chain.invoke({"query": state["query"]}).content
    return {"sentiment": sentiment}

def handle_technical(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a technical support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

def handle_billing(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a billing support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

def handle_general(state: State) -> State:
    prompt = ChatPromptTemplate.from_template(
        "Provide a general support response to the following query: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"response": response}

def escalate(state: State) -> State:
    """Escalate negative sentiment queries."""
    return {"response": "This query has been escalated to a human agent due to its negative sentiment analysis."}

def route_query(state: State) -> State:
    """Route the query to the appropriate handler based on the category and sentiment."""
    if state['sentiment'] == 'Negative':
        return "escalate"
    elif state['category'] == "Technical":
        return "handle_technical"
    elif state['category'] == "Billing":
        return "handle_billing"
    else:
        return "handle_general"

workflow = StateGraph(State)
workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_technical", handle_technical)
workflow.add_node("handle_billing", handle_billing)
workflow.add_node("handle_general", handle_general)
workflow.add_node("escalate", escalate)
workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_conditional_edges(
    "analyze_sentiment",
    route_query,
    {
        "handle_technical": "handle_technical",
        "handle_billing": "handle_billing",
        "handle_general": "handle_general",
        "escalate": "escalate"
    }
)
workflow.add_edge("handle_technical", END)
workflow.add_edge("handle_billing", END)
workflow.add_edge("handle_general", END)
workflow.add_edge("escalate", END)
workflow.set_entry_point("categorize")
app = workflow.compile()

import gradio as gr

# Define the function that integrates the workflow.
def run_customer_support(query: str) -> Dict[str, str]:
    # Wrap the input query in a dictionary
    initial_state = {"query": query}

    # Pass the initial state to the app
    result = app.invoke(initial_state)

    return {
        "category": result["category"],
        "sentiment": result["sentiment"],
        "response": result["response"],
    }

# Create a Gradio interface
def gradio_interface(query: str):
    result = run_customer_support(query)
    return (
        f"**Category**: {result['category']}\n\n"
        f"**Sentiment**: {result['sentiment']}\n\n"
        f"**Response**: {result['response']}\n\n"
    )

# Build the Gradio app
gui = gr.Interface(
    fn=gradio_interface,
    theme='Yntec/HaleyCH_Theme_Yellow_Green',
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here..."),
    outputs=gr.Markdown(),
    title="CUSTOMER SUPPORT ASSISTANT 🤖💬📞"
)

# Launch the app
if __name__ == "__main__":
    gui.launch()
