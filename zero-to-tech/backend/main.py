from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

profile = {
    "heroTitle": "关于我",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
}

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/api/profile")
def get_profile():
    return profile

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    return{
    "text": request.text,
    "score": 0.6,
    "label": "积极",
    "pinyin": "wo shi ni de 88",
    }
