from langchain_ollama import ChatOllama

model= ChatOllama(
    model="gemma3:1b",
    temperature=0,
    system="You are a very good friend.",
)


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


from langchain_core.messages import SystemMessage, trim_messages

trimmer = trim_messages(
    max_tokens=500,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)





# Define the function that calls the model
async def call_model(state: MessagesState):
    response = await model.ainvoke(state["messages"])
    #trimmer.invoke(state["messages"])
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
from langgraph.store.memory import InMemoryStore
import asyncio
store = InMemoryStore()

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, store=store)

#app = workflow.compile(checkpointer=memory)
print("Graph compiled successfully.")




### Example usage
# config = {"configurable": {"thread_id": "abc123"}}

# async def test_app():
#     query = "Hi! I'm Bob."
#     input_messages = [HumanMessage(query)]
#     output = await app.ainvoke({"messages": input_messages}, config)
#     output["messages"][-1].pretty_print()

#     query = "What's my name?"
#     input_messages = [HumanMessage(query)]
#     output = await app.ainvoke({"messages": input_messages}, config)
#     output["messages"][-1].pretty_print()

# # Ejecuta la prueba
# asyncio.run(test_app())
