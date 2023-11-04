from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import utils, models, schemas
from database import SessionLocal, engine

from typing import Annotated

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# / com mensagem de boas vindas
@app.get("/")
def root():
    return {"message": "Welcome to the gym!"}


# Listar todos os membros: GET /members
@app.get(
    "/members/", response_model=list[schemas.Member], description="List all members"
)
def get_all_members(skip: int = 0, db: Session = Depends(get_db)):
    members = utils.db_get_members(db, skip=skip)
    return members


# Obter detalhes de um membro específico: GET /members/{id}
@app.get("/member/{member_id}", response_model=schemas.Member)
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_user


# Criar um novo membro: POST /members
@app.post("/member/", status_code=201, description="Create a new member", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    
    pseudo_member_id = utils.db_get_members(db, id=member.member_id)
    
    if pseudo_member_id is not None:
        raise HTTPException(status_code=409, detail=f"Member with id {member.member_id} already exists")
    
    db_member = utils.db_create_member(db, member)
    
    return db_member


# Atualizar os detalhes de um membro: PUT /members/{id}

'''
@app.put(
    "/member/{member_id}",
    description="Update member details by identifying it by id",
    status_code=200,
)
def update_member(
    member_id: Annotated[int, Path(title="Member Id", example=0)],
    name: Annotated[str | None, Query(title="Name", example="Mario")] = None,
    birth_date: Annotated[
        str | None, Query(title="Date of birth", example="1970-01-01 00:00:00")
    ] = None,
    email: Annotated[
        str | None, Query(title="Email", example="mario@armario.com")
    ] = None,
    phone: Annotated[
        str | None, Query(title="Phone number", example="55 11 99999=9999")
    ] = None,
    cpf: Annotated[str | None, Query(title="CPF", example="12345678911")] = None,
    inscription_date: Annotated[
        str | None, Query(title="Inscription date", example="1970-01-01 00:00:00")
    ] = None,
) -> dict[str, Member]:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )

    if name == birth_date == email == phone == cpf == inscription_date == None:
        raise HTTPException(status_code=400, detail="Bad request: all params are null")

    if name is not None:
        dict_members[member_id].name = name
    if birth_date is not None:
        dict_members[member_id].birth_date = datetime.datetime.strptime(
            birth_date, "%Y-%m-%d %H:%M:%S"
        )
    if email is not None:
        dict_members[member_id].email = email
    if phone is not None:
        dict_members[member_id].phone = phone
    if cpf is not None:
        dict_members[member_id].cpf = cpf
    if inscription_date is not None:
        dict_members[member_id].inscription_date = datetime.datetime.strptime(
            inscription_date, "%Y-%m-%d %H:%M:%S"
        )

    return {"updated": dict_members[member_id]}


# Excluir um membro: DELETE /members/{id}


@app.delete("/member/{member_id}", status_code=204)
def delete_member(
    member_id: Annotated[
        int, Path(title="Member id", description="Delete an specific member by id")
    ]
) -> None:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )

    del dict_members[member_id]
    return


# Planos (Plans):
# Listar todos os planos: GET /plans


@app.get("/plans", description="List all plans")
def get_plans() -> list[Plan]:
    return list(dict_planos.values())


# Obter detalhes de um plano específico: GET /plans/{id}


@app.get("/plan/{plan_id}")
def get_plans(
    plan_id: Annotated[
        int, Path(title="Plan id", description="Get an specific plan by id", example=0)
    ]
):
    if plan_id not in dict_planos:
        raise HTTPException(
            status_code=400, detail=f"Plan with id {plan_id} does not exist"
        )

    return {plan_id: dict_planos[plan_id]}


# Criar um novo plano: POST /plans
@app.post("/plan", status_code=201, description="Create a new plan")
def post_plan(plan: Plan):
    if plan.plan_id in dict_planos:
        raise HTTPException(status_code=409, detail=f"Plan alredy exists")

    dict_planos[plan.plan_id] = plan
    print(dict_planos[plan.plan_id])
    return {"added": plan}


# Atualizar os detalhes de um plano: PUT /plans/{id}. O que será atualizado é passado nos parametros


@app.put("/plan/{plan_id}", description="Update plan details by identifying it by id")
def update_plan(
    plan_id: Annotated[int, Path(title="Plan id", example=0)],
    plan_name: Annotated[str | None, Query(title="Plan name", example="Black")] = None,
    descr: Annotated[
        str | None,
        Query(
            title="Plan description",
            example="Premium plan that allows members to use all facilities",
        ),
    ] = None,
    price: Annotated[int | None, Query(title="Price", example=200)] = None,
) -> dict[str, Plan]:
    if plan_id not in dict_planos:
        raise HTTPException(
            status_code=404, detail=f"Plan with id {plan_id} does not exist"
        )

    if descr == price == plan_name == None:
        raise HTTPException(status_code=400, detail="Bad request: all params are null")

    if plan_name is not None:
        dict_planos[plan_id].plan_name = plan_name
    if descr is not None:
        dict_planos[plan_id].descr = descr
    if price is not None:
        dict_planos[plan_id].price = price

    return {"updated": dict_planos[plan_id]}


# Excluir um plano: DELETE /plans/{id}


@app.delete("/plan/{plan_id}", status_code=204)
def update_plan(
    plan_id: Annotated[
        int, Path(title="Plan id", description="Delete an specific plan by id")
    ]
):
    if plan_id in dict_planos:
        del dict_planos[plan_id]
        return
    raise HTTPException(
        status_code=404, detail=f"Plan with id {plan_id} does not exist"
    )


# Membros de um Plano (Members in a Plan):
@app.get("/plans/all_members", description="List all members in all plans")
def query_members_by_plan() -> dict[int, list[Member]]:
    dic = {}
    for plan in dict_planos:
        dic[plan] = []
        for member in dict_members:
            if dict_members[member].plan_id == plan:
                dic[plan].append(dict_members[member])
    return dic


# Listar todos os membros de um plano específico: GET /plans/{plan_id}/members
@app.get("/plan/{plan_id}/members", description="List all members in a specific plan")
def query_members_by_specific_plan(
    plan_id: Annotated[
        int,
        Path(
            title="Plan id",
            description="Id of the plan you want to get the members of",
            example=0,
        ),
    ]
) -> list[Member]:
    if plan_id not in dict_planos:
        raise HTTPException(
            status_code=404, detail=f"Plan with id {plan_id} does not exist"
        )
    plan_members = []
    for member in dict_members:
        if dict_members[member].plan_id == plan_id:
            plan_members.append(dict_members[member])
    return plan_members


# Adicionar um membro a um plano: PUT /plans/{plan_id}/members


@app.put("/plan/{plan_id}/members/{member_id}", description="Add a member to a plan")
def add_member_to_plan(
    plan_id: Annotated[
        int,
        Path(
            title="Plan id", description="Id of the plan you want to add to", example=0
        ),
    ],
    member_id: Annotated[
        int,
        Path(
            title="Plan id", description="Id of the member you want to add", example=0
        ),
    ],
) -> dict[str, Member]:
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail="One of the given IDs does not exisdkk"
        )
    dict_members[member_id].plan_id = plan_id
    return {"updated": dict_members[member_id]}


# Remover um membro de um plano: DELETE /plans/{plan_id}/members/{member_id}


@app.delete(
    "/plan/{plan_id}/members/{member_id}",
    description="Remove a member from a plan",
    status_code=204,
)
def delete_member(
    plan_id: Annotated[
        int,
        Path(
            title="Plan id",
            description="Id of the plan you want to delete from",
            example=0,
        ),
    ],
    member_id: Annotated[
        int,
        Path(
            title="Member id",
            description="Id of the member you want to delete",
            example=0,
        ),
    ],
) -> None:
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail="One of the given IDs does not exisdkk"
        )
    if dict_members[member_id].plan_id != plan_id:
        raise HTTPException(
            status_code=400,
            detail=f"Member {member_id} does not have the plan {dict_planos[plan_id].plan_name}",
        )
    dict_members[member_id].plan_id = None
    return


# Evaluations


# Pegar todas as avaliações de um membro : GET /member/{member_id}/evaluation
@app.get(
    "/member/{member_id}/evaluations", description="List all evaluations from a member"
)
def get_all_evaluations_from_member(
    member_id: Annotated[
        int,
        Path(
            title="Member id",
            description="Id of the member you want to get the evaluations from",
            example=0,
        ),
    ]
) -> list[Evaluation]:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )
    return dict_members[member_id].evaluations


# Pegar uma avaliação pelo id dela
@app.get("/evaluation/{evaluation_id}", description="Get an evaluation by its id")
def get_evaluation_by_id(
    evaluation_id: Annotated[
        int,
        Path(
            title="Evaluation id",
            description="Id of the evaluation you want to get",
            example=0,
        ),
    ]
) -> dict[str, Evaluation]:
    if evaluation_id not in dict_evaluations:
        raise HTTPException(
            status_code=404, detail=f"Evaluation with id {evaluation_id} does not exist"
        )
    return {"evaluation": dict_evaluations[evaluation_id]}


# Pegar a N'esima avaliacao de um membro : GET /member/{member_id}/evaluation/{evaluation_n}
@app.get(
    "/member/{member_id}/evaluation/{evaluation_n}",
    description="Get the n'th evaluation from a member",
)
def get_all_evaluations_from_member(
    member_id: Annotated[
        int,
        Path(
            title="Member id",
            description="Id of the member you want the evaluations from",
        ),
    ],
    evaluation_n: Annotated[
        int,
        Path(
            title="Evaluation Number",
            description="Number of the evaluation you want to get",
        ),
    ],
) -> dict[str, Evaluation]:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )

    if evaluation_n >= len(dict_members[member_id].evaluations):
        raise HTTPException(
            status_code=404,
            detail=f"Member with id {member_id} does not have {evaluation_n} evaluations",
        )

    return {"evaluation": dict_members[member_id].evaluations[evaluation_n]}


# Criar uma nova avaliacao : POST /member/{member_id}/evaluation


@app.post(
    "/member/{member_id}/evaluation",
    status_code=201,
    description="Create a new evaluation",
)
def create_workout_evaluation(
    member_id: Annotated[
        int,
        Path(
            title="Member id",
            description="Id of the member you want add the evaluations to",
        ),
    ],
    evaluation: Evaluation,
) -> dict[str, Evaluation]:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )

    if evaluation.evaluation_id in dict_evaluations:
        raise HTTPException(
            status_code=409, detail=f"Evaluation with same id alredy exists"
        )

    dict_evaluations[evaluation.evaluation_id] = evaluation
    dict_members[member_id].evaluations.append(evaluation)

    return {"added": evaluation}


@app.delete(
    "/member/{member_id}/evaluation/{evaluation_n}",
    description="Delete the n'th evaluation from a member",
    status_code=204,
)
def get_all_evaluations_from_member(
    member_id: Annotated[
        int,
        Path(
            title="Member id",
            description="Id of the member you want to remove the evaluation from",
        ),
    ],
    evaluation_n: Annotated[
        int,
        Path(
            title="Evaluation Number",
            description="Number of the evaluation you want to remove",
        ),
    ],
) -> None:
    if member_id not in dict_members:
        raise HTTPException(
            status_code=404, detail=f"Member with id {member_id} does not exist"
        )

    if evaluation_n >= len(dict_members[member_id].evaluations):
        raise HTTPException(
            status_code=404,
            detail=f"Member with id {member_id} does not have {evaluation_n} evaluations",
        )

    evaluation_id = dict_members[member_id].evaluations[evaluation_n].evaluation_id
    dict_members[member_id].evaluations.pop(evaluation_n)
    del dict_evaluations[evaluation_id]

    return
    
'''
