from dataclasses import dataclass, field
from typing import List


@dataclass
class BenchmarkResult:

    subject: str = ""

    global_score: int = 0

    patrimonial: int = 0
    pedagogy: int = 0
    instagram: int = 0
    hook: int = 0
    cta: int = 0
    compliance: int = 0
    credibility: int = 0
    virality: int = 0

    execution_time: float = 0.0

    cost: float = 0.0

    version: str = ""

    notes: List[str] = field(default_factory=list)
    