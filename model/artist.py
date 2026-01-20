from dataclasses import dataclass

@dataclass
class Artist:
    id : int
    name : str

    def __str__(self):
        return f"{self.id}, {self.name}"

    def __eq__(self, other):
        return (self.id == other.id) and (self.name == other.name)

    def __lt__(self, other):
        return (self.id < other.id)

    def __hash__(self):
        return hash(self.id)