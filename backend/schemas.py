from typing import Any

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = "Junior BA Learner"
    email: str | None = None
    targetScore: int = 500
    weakness: str = "Grammar"
    level: str = "Foundation"


class LoginRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    targetScore: int = 500
    weakness: str = "Grammar"


class LessonPayload(BaseModel):
    id: str | None = None
    title: str
    level: str = "Foundation"
    context: str = ""
    passage: str = ""
    vocabulary: list[str] = Field(default_factory=list)
    grammar: str = ""
    questions: list[dict[str, Any]] = Field(default_factory=list)


class VocabularyPayload(BaseModel):
    id: str | None = None
    word: str
    part: str = ""
    meaningId: str = ""
    meaningEn: str = ""
    example: str = ""
    answer: str = ""


class ProgressAttempt(BaseModel):
    userId: str = "guest-user"
    module: str
    score: int
    payload: dict[str, Any] = Field(default_factory=dict)


class TextPayload(BaseModel):
    text: str = ""
    type: str = "simple"


class ChatPayload(BaseModel):
    message: str = ""
    context: dict[str, Any] = Field(default_factory=dict)


class ContextualHelpPayload(BaseModel):
    text: str = ""
    module: str = "general"
    context_type: str = "general"
    user_level: str = "beginner"
    extra_context: dict[str, Any] = Field(default_factory=dict)
