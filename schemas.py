from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EvaluationBase(BaseModel):
    evaluation_date: datetime = Field(
        description="The date of evaluation", le=datetime.now(), examples=["2021-01-01"]
    )
    weight: float = Field(
        description="The weight of member", gt=0, examples=[70.5, 80.0]
    )
    height: float = Field(
        description="The height of member", gt=0, examples=[1.70, 1.80]
    )
    fat_percentage: float | None = Field(
        default=None,
        description="The fat percentage of member, can none value",
        gt=0,
        le=100,
        examples=[15.0, 20.0],
    )
    observation: str | None = Field(
        default=None,
        description="The observation of evaluation, value can be none",
        max_length=300,
        examples=[
            "Antônio complained of pain in the back, make sure he does the exercises correctly."
        ],
    )


class EvaluationCreate(EvaluationBase):
    pass


class Evaluation(EvaluationBase):
    evaluation_id: int = Field(description="The id of evaluation", examples=["0", "1"])
    evaluation_owner_id: int = Field(
        description="The id of member", examples=["0", "1"]
    )

    model_config = {
        "from_attributes": "True",
        "json_schema_extra": {
            "examples": [
                {
                    "evaluation_id": "0",
                    "evaluation_date": "2021-01-01T00:00:00",
                    "weight": 70.5,
                    "height": 1.70,
                    "fat_percentage": 15.0,
                    "observation": "Antônio complained of pain in the back, make sure he does the exercises correctly.",
                },
                {
                    "evaluation_id": "1",
                    "evaluation_date": "2021-02-01T00:00:00",
                    "weight": 50.0,
                    "height": 1.53,
                    "fat_percentage": 20.0,
                    "observation": "Leandra wishes to get more strength in the legs, increase the weight of the exercises.",
                },
            ]
        },
    }


class MemberBase(BaseModel):
    name: str = Field(
        description="Full name of the member",
        max_length=100,
        examples=["Arthur Martins", "Antônio Carlos de Almeida"],
    )
    birth_date: datetime = Field(
        description="The birth date of member",
        le=datetime.now(),
        examples=["1999-02-01T00:00:00"],
    )
    email: str = Field(
        description="The email of member",
        max_length=100,
        examples=["arthurmsb@al.insper.edu,br"],
    )
    phone: str | None = Field(
        default=None,
        description="The phone of member",
        max_length=20,
        examples=["+55 11 99999-9999"],
    )
    cpf: str = Field(
        description="The CPF of member", max_length=11, examples=["12345678901"]
    )

    inscription_date: datetime = Field(
        description="The date of inscription",
        le=datetime.now(),
        examples=["2021-02-01T00:00:00"],
    )


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    member_id: int = Field(description="The id of member", examples=["0", "1"])
    plan_id: Optional[int] = (None,)
    evaluations: list[Evaluation] = Field(
        description="The evaluations of member",
        examples=[
            [
                {
                    "evaluation_id": "0",
                    "evaluation_date": "2021-02-01T00:00:00",
                    "weight": 70.5,
                    "height": 1.70,
                    "fat_percentage": 15.0,
                    "observation": "Antônio complained of pain in the back, make sure he does the exercises correctly.",
                },
                {
                    "evaluation_id": "1",
                    "evaluation_date": "2021-02-01T00:00:00",
                    "weight": 50.0,
                    "height": 1.53,
                    "fat_percentage": 20.0,
                    "observation": "Leandra wishes to get more strength in the legs, increase the weight of the exercises.",
                },
            ]
        ],
    )

    model_config = {
        "from_attributes": "True",
        "json_schema_extra": {
            "examples": [
                {
                    "member_id": "2",
                    "name": "Arthur Martins",
                    "birth_date": "1990-01-01T00:00:00",
                    "email": "arthurmsb@al.insper.edu.br",
                    "phone": "+55 11 99999-9999",
                    "cpf": "12345678901",
                    "inscription_date": "2021-01-01T00:00:00",
                    "plan_id": "0",
                    "evaluations": [
                        {
                            "evaluation_id": "0",
                            "evaluation_date": "2021-01-01T00:00:00",
                            "weight": 70.5,
                            "height": 1.70,
                            "fat_percentage": 15.0,
                            "observation": "Antônio complained of pain in the back, make sure he does the exercises correctly.",
                        }
                    ],
                }
            ]
        },
    }

class PlanBase(BaseModel):
    plan_name: str = Field(
        description="The name of plan, like: Basic, premimum ...",
        max_length=50,
        examples=["Basic", "Black", "Gold"],
    )
    descr: str = Field(
        description="A short description of plan",
        max_length=300,
        examples=["Black plan allow you to use any gym from our network"],
    )
    price: float = Field(
        description="The price of plan", gt=0, examples=[100.00, 200.00, 300.00]
    )


class PlanCreate(PlanBase):
    pass


class Plan(PlanBase):
    plan_id: int = Field(description="The id of plan", examples=["0", "1", "2"])
    members: list[Member] = []

    model_config = {
        "from_attributes": "True",
        "json_shemma_extra": {
            "examples": [
                {
                    "plan_id": "0",
                    "plan_name": "Basic",
                    "descr": "Basic plan allow you to use our gym",
                    "price": 100.00,
                },
                {
                    "plan_id": "1",
                    "plan_name": "Black",
                    "descr": "Black plan allow you to use any gym from our network",
                    "price": 200.00,
                },
            ]
        },
    }


