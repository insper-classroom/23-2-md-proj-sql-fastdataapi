from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date

class Plan(BaseModel):
    plan_id : UUID
    plan_name : str = Field(
        'The name of plan, like: Basic, premimum ...', max_length=50
    )
    descr : str = Field(
        'A short description of plan', max_length=300
    )   
    price : float = Field(
        'The price of plan', gt=0
    )
    
class Evaluation(BaseModel):
    evaluation_id: UUID = Field(
        'The evaluation id, an identifier of evaluation'
    )
    evaluation_date: date = Field(
        'The date of evaluation', le=date.today()
    )
    weight: float = Field(
        'The weight of member', gt=0
    )
    height: float = Field(
        'The height of member', gt=0
    )
    fat_percentage: float | None = Field(
        'The fat percentage of member, can none value', gt=0
    )
    observation: str | None = Field(
        'The observation of evaluation, value can be none', max_length=300
    )

class Member(BaseModel):
    member_id: UUID
    name: str = Field(
        'Full name of the member', max_length=100
    )
    birth_date: date = Field(
        'The birth date of member', le=date.today()
    )
    email: str = Field(
        'The email of member', max_length=100
    )
    phone: str | None = Field(
        'The phone of member', max_length=20
    )
    inscription_date: date = Field(
        'The date of inscription', le=date.today()
    )
    plan_id: UUID = Field(
        'The plan id of member'
    )
    evaluations : list[Evaluation] = Field(
        'The evaluations of member'
    )