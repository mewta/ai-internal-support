from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.rag.answerer import answer_question

router = APIRouter()


@router.post("/ask")
def ask_question(
    question: str,
    user=Depends(get_current_user),
):
    return answer_question(
        question=question,
        user_role=user["role"],
    )
