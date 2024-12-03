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


@dataclass
class TaskWithGroup:
    group_id: int
    task_id: int
    title: str
    description: str
    assigned: list
    status: str
    date: str
