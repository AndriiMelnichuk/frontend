from dataclasses import dataclass

@dataclass
class Task:
    title: str
    description: str
    assigned: str
    created: str
    status: str
    date: str

@dataclass
class Group:
    title: str
    administrator: str | list