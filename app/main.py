from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import pydantic
import requests
import json
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


token: str = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAiaHR0cHM6Ly9hdXRoLnR1cnRsZW1vdmVzLmFpIiwgInN1YiI6ICJQYW5nZWEgSW50ZXJuYWwgQXV0aCIsICJhdWQiOiAicGFuZ2VhLW1hc3RlciIsICJhcHAiOiAicGFuZ2VhX21haW4iLCAianRpIjogIjY2ZWFhOGYxMTQ1ZjY2YWE1NjAzMWYwNSIsICJleHAiOiAxNzI5NjY0NDk1LjYzMDc2OSwgImlhdCI6IDE3MjcwNzI0OTUuNjMwNzY5LCAic2NvcGUiOiBbImFkbWluIl19.0779a6a9b396cc37beb826507ef433acc3c22b2cf3334e86189248bee9f3d94d"


def responseFromAira(query: str):
    url = "https://ca-aira-backend-temp-eastus.ambitiouswave-dd67970c.eastus.azurecontainerapps.io/aira-api/v1/chat"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "ask_openai": False,
        "query": "what is the university name?",
        "regenerate_count": 0,
        "user_id": "66eaa8f1145f66aa56031f05",
    }
    resp = requests.post(url=url, headers=headers, data=json.dumps(payload))
    url_response = resp.json()
    for i in url_response["answer"]:
        yield i
        asyncio.sleep(0.04)



@app.post("/response")
async def get(payload: Query):
    return EventSourceResponse(responseFromAira(query=payload.query))
