from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
import uuid


class Role(str, Enum):
    user = "user"
    admin = "admin"


class Auth(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    hashed_password: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    role: Role = Field(default=Role.user, nullable=False)
