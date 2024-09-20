from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import pydantic
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(pydantic.BaseModel):
    query: str


async def waypoints_generator(query : str):
    for i in query:
        yield i
        await asyncio.sleep(0.03)


@app.post("/get-waypoints")
async def root(payload : Query):
    return StreamingResponse(waypoints_generator(payload.query), media_type="text/event-stream")



    