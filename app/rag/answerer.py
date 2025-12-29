from app.rag.retriever import retrieve_chunks
from app.core.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.llm.groq_client import generate_answer


def answer_question(question: str, user_role: str):
    chunks = retrieve_chunks(question, user_role=user_role)

    if not chunks:
        return {
            "answer": "I don’t have enough information in the provided documents.",
            "sources": [],
        }

    # Build context from retrieved chunks
    context = "\n\n".join(
        f"[{c['file']}] {c['content']}"
        for c in chunks
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )

    answer = generate_answer(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    sources = [
        {
            "file": c["file"],
            "role": c["role"],
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }

