from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI()
#hiiii

# --- CPU only ---
device = "cpu"

# --- Hugging Face Model ---
model_name = "google/flan-t5-small"  # You can change this if needed
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

# --- Request schema ---
class Query(BaseModel):
    question: str

# --- API endpoint ---
@app.post("/ask")
def ask_ai(query: Query):
    try:
        # Tokenize input
        inputs = tokenizer(query.question, return_tensors="pt").to(device)
        # Generate response
        outputs = model.generate(**inputs, max_new_tokens=150)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # ✅ Return with key 'answer' for frontend
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"⚠️ Local model error: {e}"}
