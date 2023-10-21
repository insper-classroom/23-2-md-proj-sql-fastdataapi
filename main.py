from fastapi import FastAPI, Body, Path, Query
from typing import Annotated
from shemas import Member, Plan, Evaluation

app = FastAPI()

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
    print("get all plans")

#Obter detalhes de um plano específico: GET /plans/{id}
@app.get("/plans/{plan_id}")
def get_plans(plan_id):
    print(f"get plan of id {plan_id}")

#Criar um novo plano: POST /plans
@app.post("/plans")
def post_plan(plan: Plan):
    print(f"add plan {plan}")

#Atualizar os detalhes de um plano: PUT /plans/{id}
@app.put("/plans/{plan_id}")
def update_plan(plan_id: int, plan_name : str, descr : str):
    print(f"update plan {plan_id}")

#Excluir um plano: DELETE /plans/{id}
@app.delete("/plans/{plan_id}")
def update_plan(plan_id: int, plan_name : str, descr : str):
    print(f"update plan {plan_id}")

#Membros de um Plano (Members in a Plan):
@app.get("/plans/all_members/")
def query_members_by_plan(plan_name: str):
    print(f"get all members of plans {plan_name}")

#Listar todos os membros de um plano específico: GET /plans/{plan_id}/members
@app.get("/plans/{plan_id}/members")
def query_members_by_specific_plan(plan_name: str):
    print(f"get all members of plan {plan_name}")

#Adicionar um membro a um plano: POST /plans/{plan_id}/members
@app.get("/plans/{plan_id}/members/{member_id}") 
def get_all_members(plan_id: int, member_id:int):
    print(f"add member ")

#Remover um membro de um plano: DELETE /plans/{plan_id}/members/{member_id}
@app.delete("/plans/{plans_id}/members/{member_id}")
def delete_member():
    print(f"delete member {member_id} from plan {plan_id}")
