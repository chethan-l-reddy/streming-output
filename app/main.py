from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
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

straming_data : str = "Amidst the bustling chaos of city life, where the cacophony of honking horns and the rhythmic clatter of footsteps create a vibrant backdrop, there exists a hidden world of stories waiting to be discovered. Each person rushing by carries with them a unique narrative, woven from dreams, struggles, and triumphs that often go unnoticed in the fast-paced rush of modern existence. Street vendors call out their wares, the aroma of freshly baked bread mingling with the sharp scent of roasted coffee, tempting passersby to pause for just a moment. Artists paint vibrant murals on weathered walls, transforming mundane spaces into visual feasts that inspire conversation and provoke thought. In small cafes, friends gather to share laughter and secrets, while strangers exchange fleeting glances, each interaction a potential spark of connection in the tapestry of urban life. As the sun sets, casting a warm glow over the skyline, the city begins to pulse with an energy all its own, where nightlife awakens and possibilities unfold like petals in bloom. It’s in these moments, between the noise and the silence, that the heart of the city truly reveals itself, reminding us of the beauty and complexity that lies beneath the surface."

async def waypoints_generator():
    for i in straming_data.split(" "):
        yield i
        await asyncio.sleep(1)


@app.get("/get-waypoints")
async def root():
    return StreamingResponse(waypoints_generator(), media_type="text/event-stream")

@app.get("/response")
async def get():
    return EventSourceResponse(waypoints_generator())

