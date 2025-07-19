from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/query", tags=["Query"])

class QueryRequest(BaseModel):
    question: str
    definitions: List[str]

@router.post("/analyze")
def analyze_query(req: QueryRequest):
    # TODO: Add real logic later
    return {
        "summary": f"You asked: {req.question}",
        "filters_applied": req.definitions,
        "sample_output": [
            {"product": "Jeans", "sold": 120, "rate": 999},
            {"product": "Shirt", "sold": 80, "rate": 599},
        ],
    }
