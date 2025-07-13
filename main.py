# --- Expose as a web backend using FastAPI ---
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from modelo import app
from langchain_core.messages import HumanMessage
import uvicorn

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://ju4ndiegos.github.io",
]


web_app = FastAPI()

web_app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@web_app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message","")
    config = data.get("config", {})
    output = await app.ainvoke({"messages":[HumanMessage(message)]}, config)
    print(output)
    return JSONResponse(content=output["messages"][-1].content)
