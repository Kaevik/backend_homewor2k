from dataclasses import dataclass, field
from typing import List

from app.quiz.models import Theme, Question
from app.admin.models import Admin

@dataclass
class Database:
    themes: List[Theme] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)
    admins: List[Admin] = field(default_factory=list)

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    @property
    def next_question_id(self) -> int:
        return len(self.questions) + 1

    @property
    def next_admin_id(self) -> int:
        return len(self.admins) + 1

    def clear(self):
        self.themes.clear()
        self.questions.clear()
        self.admins.clear()
