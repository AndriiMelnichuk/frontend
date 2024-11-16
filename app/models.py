from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    description: str
    assigned: list
    status: str
    date: str

@dataclass
class Group:
    id: int
    name: str
