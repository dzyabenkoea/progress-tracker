from typing import Union
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/trackers")
def trackers():
    return [
        {
            "id": 12333,
            "name": 'Трекер 1',
            "points": [True, True, False, False, False]
        },
        {
            "id": 12334,
            "name": 'Трекер 2',
            "points": [False, False, False, False, False]
        }
    ]


@app.get("/trackers/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
