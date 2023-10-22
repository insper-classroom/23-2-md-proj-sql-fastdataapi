from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Annotated
from shemas import Member, Plan, Evaluation
import json

app = FastAPI()

dict_planos = {}
dict_membros = {}

#Listar todos os membros: GET /members
@app.get("/members")
async def get_all_members():
    print("get all members")
    
#Obter detalhes de um membro específico: GET /members/{id}
@app.get("/members/{member_id}")
def get_member(member_id):
    print(f"get member of id {member_id} members")

#Criar um novo membro: POST /members
@app.post("/members")
def get_member(member : Member):
    print(f"post member {member}")

#Atualizar os detalhes de um membro: PUT /members/{id}
@app.put("/members/{member_id}")
def update_member(member_id: int, member_name: str):
    print(f"update member of {member_id}")

#Excluir um membro: DELETE /members/{id}
@app.delete("/members/{member_id}")
def delete_member(member_id):
    print(f"delete member of {member_id}")
    
#Planos (Plans):
#Listar todos os planos: GET /plans
@app.get("/plans")
def get_plans():
    return {plans: dict_planos}

#Obter detalhes de um plano específico: GET /plans/{id}
@app.get("/plan/{plan_id}")
def get_plans(plan_id:int):
    print(f"get plan of id {plan_id}")

#Criar um novo plano: POST /plans
@app.post("/plan")
def post_plan(plan: Plan):
    
    if plan.plan_id in dict_planos:
        HTTPException(status_code=400, detail=f"Plan alredy exists")

    dict_planos[plan.plan_id] = plan  #.model_dump()
    #with open("planos.json", "w") as f:
    #    json.dump(dict_planos, f)
    print(dict_planos[plan.plan_id])
    return {"added":plan}

#Atualizar os detalhes de um plano: PUT /plans/{id}
@app.put("/plan/{plan_id}")
def update_plan(plan_id: int, plan_name : str, descr : str):
    print(f"update plan {plan_id}")

#Excluir um plano: DELETE /plans/{id}
@app.delete("/plan/{plan_id}")
def update_plan(plan_id: int, plan_name : str, descr : str):
    print(f"update plan {plan_id}")

#Membros de um Plano (Members in a Plan):
@app.get("/plans/all_members/")
def query_members_by_plan(plan_name: str):
    print(f"get all members of plans {plan_name}")

#Listar todos os membros de um plano específico: GET /plans/{plan_id}/members
@app.get("/plan/{plan_id}/members")
def query_members_by_specific_plan(plan_name: str):
    print(f"get all members of plan {plan_name}")

#Adicionar um membro a um plano: POST /plans/{plan_id}/members
@app.get("/plan/{plan_id}/members/{member_id}") 
def get_all_members(plan_id: int, member_id:int):
    print(f"add member ")
#Remover um membro de um plano: DELETE /plans/{plan_id}/members/{member_id}
@app.delete("/plan/{plan_id}/members/{member_id}")
def delete_member(plan_id:int , member_id:int):
    print(f"delete member {member_id} from plan {plan_id}")


#Evaluations
