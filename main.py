from fastapi import Depends, FastAPI, HTTPException, Path, Query
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
    "/members/", response_model=list[schemas.Member], description="List all members", tags=["Members"]
)
def get_all_members(db: Session = Depends(get_db)):
    members = utils.db_get_members(db)
    return members


# Obter detalhes de um membro específico: GET /members/{id}
@app.get("/member/{member_id}", response_model=schemas.Member, tags=["Members"])
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_user


# Obter detalhes de um membro por nome: GET /members/{nome}
@app.get("/member/name/{member_name}", response_model=list[schemas.Member], tags=["Members"])
def get_member_name(member_name: str, db: Session = Depends(get_db)):
    db_user = utils.db_get_members_name(db, name=member_name)
    return db_user


# Criar um novo membro: POST /members
@app.post(
    "/member/",
    status_code=201,
    description="Create a new member",
    response_model=schemas.MemberCreate,
    tags=["Members"]
)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = utils.db_create_member(db, member)

    print(f"db_member: {db_member}")

    return db_member


# Atualizar os detalhes de um membro: PUT /members/{id}
@app.put(
    "/member/{member_id}",
    description="Update member details by identifying it by id",
    status_code=200,
    tags=["Members"]
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
    db: Session = Depends(get_db),
) -> dict[str, schemas.Member]:
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return {
        "updated": utils.db_update_member(
            db,
            member_id=member_id,
            name=name,
            birth_date=birth_date,
            email=email,
            phone=phone,
            cpf=cpf,
            inscription_date=inscription_date,
        )
    }


# Excluir um membro: DELETE /members/{id}
@app.delete("/member/{member_id}", status_code=204, tags=["Members"])
def delete_member(
    member_id: Annotated[
        int, Path(title="Member id", description="Delete an specific member by id")
    ],
    db: Session = Depends(get_db),
) -> None:
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")
    utils.db_delete_members(db, member_id)
    return


# Planos (Plans):
# Listar todos os planos: GET /plans
@app.get("/plans", description="List all plans", tags=["Plans"])
def get_plans(db: Session = Depends(get_db)) -> list[schemas.Plan]:
    return utils.db_get_plan(db)


# Obter detalhes de um plano específico: GET /plans/{id}
@app.get("/plan/{plan_id}", tags=["Plans"])
def get_plan(
    plan_id: Annotated[
        int, Path(title="Plan id", description="Get an specific plan by id", example=0)
    ],
    db: Session = Depends(get_db),
):
    db_plan = utils.db_get_plan(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan


@app.get("/plan/name/{plan_name}", response_model=list[schemas.Member], tags=["Plans"])
def get_plan_name(plan: str, db: Session = Depends(get_db)):
    db_plan = utils.db_get_plan_name(db, name=plan)
    return db_plan


# Criar um novo plano: POST /plans
@app.post("/plan", status_code=201, description="Create a new plan", tags=["Plans"])
def post_plan(
    plan: schemas.PlanCreate, db: Session = Depends(get_db)
) -> dict[str, schemas.Plan]:
    plan = utils.db_post_plan(db, plan)
    return {"added": plan}


# Atualizar os detalhes de um plano: PUT /plans/{id}. O que será atualizado é passado nos parametros
@app.put("/plan/{plan_id}", description="Update plan details by identifying it by id", tags=["Plans"])
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
    db: Session = Depends(get_db),
) -> dict[str, schemas.Plan]:
    if descr == price == plan_name == None:
        raise HTTPException(status_code=400, detail="Bad request: all params are null")

    db_plan = utils.db_get_plan(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    return {
        "updated": utils.db_update_plan(
            db, plan_id=plan_id, plan_name=plan_name, descr=descr, price=price
        )
    }


# Excluir um plano: DELETE /plans/{id}
@app.delete("/plan/{plan_id}", status_code=204, tags=["Plans"])
def delete_plan(
    plan_id: Annotated[
        int, Path(title="Plan id", description="Delete an specific plan by id")
    ],
    db: Session = Depends(get_db),
):
    db_plan = utils.db_get_plan(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="plan not found")
    utils.db_delete_plan(db, plan_id)
    return


# Adicionar um membro a um plano: PUT /plans/{plan_id}/members
@app.put("/plan/{plan_id}/members/{member_id}", status_code=201,description="Add a member to a plan", tags=["Member plans"])
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
    db: Session = Depends(get_db),
) -> dict[str, schemas.Member]:
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")
    db_plan = utils.db_get_plan(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"updated": utils.db_add_member_to_plan(db, member_id, plan_id)}


@app.delete("/members/{member_id}/cancel_plan", status_code=204, description="Remove a member from a plan", tags=["Member plans"])
def add_member_to_plan(
    member_id: Annotated[
        int,
        Path(
            title="Plan id", description="Id of the member you want to add", example=0
        ),
    ],
    db: Session = Depends(get_db),
) -> None:
    db_user = utils.db_get_members(db, id=member_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Member not found")
    utils.db_remove_plan_from_member(db, member_id)
    return


