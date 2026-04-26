from dataclasses import dataclass, field
from typing import Any


@dataclass
class Lesson:
    id: str
    title: str
    level: str = "Foundation"
    context: str = ""
    passage: str = ""
    vocabulary: list[str] = field(default_factory=list)
    grammar: str = ""
    questions: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class VocabularyItem:
    id: str
    word: str
    part: str = ""
    meaningId: str = ""
    meaningEn: str = ""
    example: str = ""
    answer: str = ""
