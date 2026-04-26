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


@dataclass
class LearningJourney:
    id: str
    user_id: str
    current_level: str = "Beginner 1"
    overall_score: float = 0
    total_exercises: int = 0
    learning_streak: int = 0
    weakest_skill: str = "grammar"
    strongest_skill: str = "reading"
    next_recommended_module: str = "grammar"


@dataclass
class SkillJourney:
    id: str
    user_id: str
    skill_type: str
    current_stage: str = "Foundation"
    current_level: str = "Beginner 1"
    average_score: float = 0
    completed_count: int = 0
    total_time_spent: int = 0
    next_action: str = ""
    status: str = "not_started"
