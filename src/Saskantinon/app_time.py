#! python
"""
AI-generated. Time management for a science fiction setting.
"""

import datetime
from typing import List, Dict


class Moon:
    def __init__(self, name: str, orbital_period: int) -> None:
        self.name = name
        self.orbital_period = orbital_period  # Days it takes to complete one orbit
        self.phase = 0.0  # Phase ranges from 0 (New Moon) to 1 (Full Moon)

    def update_phase(self, days_passed: int) -> None:
        self.phase = (days_passed % self.orbital_period) / self.orbital_period


class TimeManager:
    def __init__(self, start_date: datetime.date = None) -> None:
        self.start_date = start_date or datetime.date(2100, 1, 1)
        self.current_date = self.start_date
        self.moons: List[Moon] = [
            Moon("Alpha", 27),
            Moon("Beta", 15),
            Moon("Gamma", 33),
            Moon("Delta", 21),
            Moon("Epsilon", 45),
            Moon("Zeta", 18),
            Moon("Eta", 60),
            Moon("Theta", 90),
        ]

    def advance_time(self, days: int) -> None:
        self.current_date += datetime.timedelta(days=days)
        days_elapsed = (self.current_date - self.start_date).days
        for moon in self.moons:
            moon.update_phase(days_elapsed)

    def get_moon_phases(self) -> Dict[str, float]:
        return {moon.name: moon.phase for moon in self.moons}

    def find_conjunctions(self) -> List[str]:
        # A conjunction occurs when moons are near-full at the same time
        return [moon.name for moon in self.moons if 0.9 <= moon.phase <= 1.0]

    def __str__(self) -> str:
        moon_phases = "\n".join(
            f"{moon}: {phase:.2f}" for moon, phase in self.get_moon_phases().items()
        )
        return f"Date: {self.current_date}\nMoon Phases:\n{moon_phases}"
