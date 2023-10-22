from fastapi import FastAPI, Body, Path, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from shemas import Member, Plan, Evaluation
import datetime

app = FastAPI()

plano_teste = Plan(plan_id = 0, plan_name = "Basic", descr = "Basic plan allow you to use our gym", price= 100)
dict_planos = {plano_teste.plan_id : plano_teste}

membro_teste = Member(member_id = 1, name = 'Fulano',birth_date = datetime.datetime(1990,1,1),email='arthurmsb@al.insper.edu,br',phone='+55 11 99999-9999',cpf='12345678901',inscription_date=datetime.datetime(2021,1,1),plan_id = 1,evaluations = [])
dict_members = {membro_teste.member_id : membro_teste}

#Listar todos os membros: GET /members
@app.get("/members")
def get_all_members():
    return {"members":dict_members}
    
#Obter detalhes de um membro específico: GET /members/{id}
@app.get("/member/{member_id}")
def get_member(member_id : int):
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")

    return {member_id:dict_members[member_id]}

#Criar um novo membro: POST /members
@app.post("/member")
def get_member(member : Member):
    if member.member_id in dict_members:
        raise HTTPException(status_code=400, detail=f"Member alredy exists")

    dict_members[member.member_id] = member
    return {"added":member}

#Atualizar os detalhes de um membro: PUT /members/{id}
@app.put("/member/{member_id}")
def update_member(member_id: int, member_name: str):
    print(f"update member of {member_id}")

#Excluir um membro: DELETE /members/{id}
@app.delete("/member/{member_id}")
def delete_member(member_id: int):
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")

    del dict_members[member_id]
    return {"deleted":member_id}
    
#Planos (Plans):
#Listar todos os planos: GET /plans
@app.get("/plans")
def get_plans():
    return {"plans": dict_planos}

#Obter detalhes de um plano específico: GET /plans/{id}
@app.get("/plan/{plan_id}")
def get_plans(plan_id:int):

    if plan_id not in dict_planos:
        raise HTTPException(status_code=400, detail=f"Plan with id {plan_id} does not exist")
    
    return {plan_id:dict_planos[plan_id]}


#Criar um novo plano: POST /plans
@app.post("/plan")
def post_plan(plan: Plan):
    
    if plan.plan_id in dict_planos:
        raise HTTPException(status_code=404, detail=f"Plan alredy exists")

    dict_planos[plan.plan_id] = plan
    print(dict_planos[plan.plan_id])
    return {"added":plan}

#Atualizar os detalhes de um plano: PUT /plans/{id}

#So consegui mudando para um patch. PROBLEMAS = precisa de todos os itens do plano. Corrigir quando possível
@app.patch("/plan/{plan_id}", response_model=Plan)
def update_plan(plan_id: int,plan: Plan) -> dict[str, Plan]:

    if plan_id not in dict_planos:
        raise HTTPException(status_code=400, detail=f"Plan with id {plan_id} does not exist")

    plan_data = dict_planos[plan_id]
    stored_plan_model = plan_data.copy()
    updated_data = plan.dict(exclude_unset=True)
    updated_plan = stored_plan_model.copy(update=updated_data)
    dict_planos[plan_id] = jsonable_encoder(updated_plan)
    return updated_plan

#Excluir um plano: DELETE /plans/{id}
@app.delete("/plan/{plan_id}")
def update_plan(plan_id: int):
    if plan_id in dict_planos:
        del dict_planos[plan_id]
        return {"deleted":plan_id}
    raise HTTPException(status_code=404, detail=f"Plan with id {plan_id} does not exist")


#Membros de um Plano (Members in a Plan):
@app.get("/plans/all_members/")
def query_members_by_plan(plan_name: str):
    print(f"get all members of plans {plan_name}")

#Listar todos os membros de um plano específico: GET /plans/{plan_id}/members
@app.get("/plan/{plan_id}/members")
def query_members_by_specific_plan(plan_name: str):
    print(f"get all members of plan {plan_name}")

#Adicionar um membro a um plano: POST /plans/{plan_id}/members
@app.put("/plan/{plan_id}/members/{member_id}") 
def get_all_members(plan_id: int, member_id:int):
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(status_code=404, detail="One of the given IDs does not exisdkk")
    dict_members[member_id].plan_id = plan_id
    return {"updated": dict_members[member_id]}
    
#Remover um membro de um plano: DELETE /plans/{plan_id}/members/{member_id}
@app.delete("/plan/{plan_id}/members/{member_id}")
def delete_member(plan_id:int , member_id:int):
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(status_code=404, detail="One of the given IDs does not exisdkk")
    if dict_members[member_id].plan_id != plan_id:
        raise HTTPException(status_code=400, detail=f"Member {member_id} does not have the plan {dict_planos[plan_id].plan_name}")
    dict_members[member_id].plan_id = None
    return {"deleted": f"plan {dict_planos[plan_id].plan_name} from member {member_id}"}
    


#Evaluations

