from fastapi import APIRouter, HTTPException, status
from app.models.schemas import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter()

# DEV-ONLY USERS (NO HASHING YET)
FAKE_USERS = {
    "eng@company.com": {
        "password": "eng123",
        "role": "engineering",
    },
    "ops@company.com": {
        "password": "eng123",
        "role": "operations",
    },
    "admin@company.com": {
        "password": "eng123",
        "role": "admin",
    },
}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = FAKE_USERS.get(data.email)

    if not user or data.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {
            "sub": data.email,
            "role": user["role"],
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
    }


