from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from datetime import timedelta

from src.database import get_session
from src.models.auth import Auth, Role
from src.utils.jwt import create_access_token
from src.utils.password import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # default token expiry


# -----------------------------
# Signup endpoint
# -----------------------------
@router.post("/signup")
async def signup(
    email: str,
    password: str,
    role: Role = Role.user,  # default role is 'user'
    session: AsyncSession = Depends(get_session),
):
    # Check if email is already registered
    result = await session.execute(select(Auth).where(Auth.email == email))
    existing_auth = result.scalar_one_or_none()
    if existing_auth:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new auth record
    new_auth = Auth(
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )

    session.add(new_auth)
    await session.commit()
    await session.refresh(new_auth)

    # Create JWT token
    token_data = {"id": str(new_auth.id), "role": new_auth.role.value}
    token = create_access_token(
        data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "token": token,
        "id": str(new_auth.id),
        "role": new_auth.role.value,
    }


# -----------------------------
# Signin endpoint
# -----------------------------
@router.post("/signin")
async def signin(
    email: str, password: str, session: AsyncSession = Depends(get_session)
):
    # Find user by email
    result = await session.execute(select(Auth).where(Auth.email == email))
    auth: Optional[Auth] = result.scalar_one_or_none()
    if not auth or not verify_password(password, auth.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    token_data = {"id": str(auth.id), "role": auth.role.value}
    token = create_access_token(
        data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "token": token,
        "id": str(auth.id),
        "role": auth.role.value,
    }
