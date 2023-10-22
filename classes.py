from pydantic import BaseModel

class Member(BaseModel):
    name: str
    age: int


class Plan(BaseModel):
    plan_name : str
    descr : str
    members : list[Member]


