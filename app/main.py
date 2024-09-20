from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from asyncio import sleep
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_text: str = '''
Many times when we have a requirement to send continuous stream of data from sever to the client we have majorly three options available of \n
which are pooling the data at the client side, web-sockets or server-sent events(SSE). Each one of them have its own pros & cons. Pooling \n
put unnecessary load on server when there is no data to be sent whereas websockets can be harder to scale & at the same time SSE is unidirec
'''

async def waypoints_generator():
    for i in temp_text:
        yield i
        if i == "\n":
            await sleep(1)


@app.get("/get-waypoints")
async def root():
    return StreamingResponse(waypoints_generator(), media_type="text/event-stream")



    