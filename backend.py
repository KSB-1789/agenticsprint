from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_ai(query: Query):
    # This is where Kritika's model will come later
    return {"answer": f"🤖 Dummy response to: {query.question}"}
