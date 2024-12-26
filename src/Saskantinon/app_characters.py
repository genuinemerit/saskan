#! python
"""
AI-generated characters for a science fiction setting.

# Example usage:
# generator = CharacterGenerator()
# new_character = generator.generate_random_character()
# print(new_character)
"""

import random


class Character:
    def __init__(
        self,
        name: str,
        species: str,
        traits: list[str],
        skills: list[str],
        affiliations: list[str],
    ) -> None:
        self.name = name
        self.species = species  # "Huum", AI, or other species
        self.traits = traits  # Physical and personality traits
        self.skills = skills  # Special abilities or professions
        self.affiliations = affiliations  # Factions, groups, or alliances

    def __str__(self) -> str:
        details = {
            "Name": self.name,
            "Species": self.species,
            "Traits": ", ".join(self.traits),
            "Skills": ", ".join(self.skills),
            "Affiliations": ", ".join(self.affiliations),
        }
        return "\n".join(f"{key}: {value}" for key, value in details.items())


class CharacterGenerator:
    def __init__(self):
        self.species_list = [
            "Huum",
            "Maken",
            "Evolved Reptile",
            "Sentient AI",
            "Hybrid",
        ]
        self.traits_pool = [
            "Brave",
            "Clever",
            "Cunning",
            "Empathetic",
            "Resilient",
            "Charismatic",
        ]
        self.skills_pool = [
            "Survivalist",
            "Technologist",
            "Diplomat",
            "Strategist",
            "Medic",
            "Builder",
        ]
        self.affiliations_pool = [
            "Free City",
            "Solarpunk Collective",
            "Handmaid Resistance",
            "Corporate Entity",
        ]

    def generate_random_character(self, name=None):
        name = name or f"Character-{random.randint(1000, 9999)}"
        species = random.choice(self.species_list)
        traits = random.sample(self.traits_pool, k=random.randint(1, 3))
        skills = random.sample(self.skills_pool, k=random.randint(1, 3))
        affiliations = random.sample(self.affiliations_pool, k=random.randint(1, 2))
        return Character(name, species, traits, skills, affiliations)
