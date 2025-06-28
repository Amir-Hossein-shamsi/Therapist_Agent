import os
from getpass import getpass
from typing import TypedDict,Annotated,Literal
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel,Field
from dotenv import load_dotenv
load_dotenv()
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")




llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.0,
    )


class MessageClasifier(BaseModel):
    message_type:Literal["emotional","logical"]= Field(...,description="Classify if  the message requires an emotinal or logical response.")

class State(TypedDict):
    messages: Annotated[list,add_messages]
    message_type: str | None


def classify_message(state:State): 
    last_message = state["messages"][-1] if state["messages"] else ""
    classifier_llm = llm.with_structured_output(MessageClasifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or requires empathy.
            - 'logical': if it asks for facts, information, logical analystis, or practical solutions.
            """
        },
        {
            "role": "user",
            "content": last_message.content
        }
    ])

    return {
        "message_type": result.message_type
    }

def router(state: State):
    message_type = state.get("message_type",'logical')
    if message_type=="emotional":
        return {"next": "therapist_agent"}
    return {"next": "logical_agent"}


def therapist_agent(state:State) :
    last_message=state["messages"][-1]

    messages=[
        {
            "role":"system",
            "content":"""
                You are a compassion therapist.Focus on the emotional aspects of user's message.
                Show empathy, validate their feeling, and help them process their emotions.
                Ask thoughtful questions to help them explore their feelings more deeply.
                Avoid giving logical solutions unless explicitly asked.
            """
        },
        {
            "role":"user",
            "content":last_message.content

        }
    ]
    
    reply= llm.invoke(messages)
    return {"messages":[{"role":"assistant","content":reply.content}]}


def logical_agent(state: State):
    last_message=state["messages"][-1]

    messages = [
        {"role": "system",
        "content": """You are a purely logical assistant. Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""
        },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    
    reply= llm.invoke(messages)
    return {"messages":[{"role":"assistant","content":reply.content}]}


grapph_builder=StateGraph(State)

grapph_builder.add_node("classifier",classify_message)
grapph_builder.add_node("router",router)
grapph_builder.add_node("therapist",therapist_agent)
grapph_builder.add_node("logical",logical_agent)

grapph_builder.add_edge(START,'classifier')
grapph_builder.add_edge('classifier','router')
grapph_builder.add_conditional_edges(
    "router",
    lambda state: state.get('next'),
    {"therapist_agent":"therapist","logical_agent":"logical"}
)

grapph_builder.add_edge("therapist",END)
grapph_builder.add_edge("logical",END)

graph=grapph_builder.compile()

def run_agent():
    state = {
        "messages": [],
        "message_type": None
    }
    while True:
        # Invoke the graph with the current state
        user_input=input("Messages: ")
        if user_input=="exit":
            print("bye")
            break
        state["messages"].append({"role": "user", "content": user_input})
        state = graph.invoke(state)
    
        if state.get('messages') and len(state['messages']) > 0:
            last_messages=state['messages'][-1]
            print(f"Assistant : ",{ last_messages.content})



if __name__=="__main__":
    run_agent()