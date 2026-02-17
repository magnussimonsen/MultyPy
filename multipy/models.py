from dataclasses import dataclass, field
from enum import Enum, auto

class GameMode(Enum):
    SIMPLE = auto()
    NORMAL = auto()

@dataclass
class Settings:
    table_range: int = 10
    max_questions: int = 10
    time_limit: int = 30
    game_mode: GameMode = GameMode.SIMPLE

@dataclass
class SessionResults:
    total_questions: int = 0
    correct_answers: int = 0
    mistakes: int = 0
    elapsed_time: float = 0.0
    
    @property
    def cpm(self) -> float:
        if self.elapsed_time > 0:
            return (self.correct_answers / self.elapsed_time) * 60
        return 0.0
