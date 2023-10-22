from fastapi import FastAPI, Body, Path, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from shemas import Member, Plan, Evaluation
import datetime

app = FastAPI()

plano_0 = Plan(plan_id = 0, plan_name = "Basic", descr = "Basic plan allow you to use our gym", price= 100)
plano_1 = Plan(plan_id = 1, plan_name = "Plus", descr = "Acess to a personal trainer up to two times a week", price= 150)
dict_planos={
                plano_0.plan_id : plano_0,
                plano_1.plan_id : plano_1
            }

membro_0 = Member(member_id = 0, name = 'Fulano',birth_date = datetime.datetime(1990,1,1),email='fulano@al.insper.edu,br',phone='+55 11 99999-9999',cpf='12345678901',inscription_date=datetime.datetime(2021,1,1),plan_id = 0,evaluations = [])
membro_1 = Member(member_id = 1, name = 'Sincrano',birth_date = datetime.datetime(1970,1,1),email='sincrano@al.insper.edu,br',phone='+55 11 99999-9999',cpf='12345678991',inscription_date=datetime.datetime(2021,1,1),plan_id = 1,evaluations = [])
dict_members = {
                    membro_0.member_id : membro_0,
                    membro_1.member_id : membro_1,
                }

dict_evaluations = {}

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
def create_member(member : Member):
    if member.member_id in dict_members:
        raise HTTPException(status_code=409, detail=f"Member with same id alredy exists")

    dict_members[member.member_id] = member
    return {"added":member}

#Atualizar os detalhes de um membro: PUT /members/{id}
@app.put("/member/{member_id}")
def update_member(member_id: int,
                  name: str | None = None,
                  birth_date : str | None = None,
                  email : str| None = None,
                  phone : str | None = None,
                  cpf : str | None = None,
                  inscription_date : str | None = None) -> dict[str,Member]:

    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")

    if name == birth_date == email == phone ==cpf == inscription_date == None:
        raise HTTPException(status_code=400, detail="Bad request: all params are null")
    
    if name is not None:
        dict_members[member_id].name = name
    if birth_date is not None:
            dict_members[member_id].birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S")
    if email is not None:
        dict_members[member_id].email = email
    if phone is not None:
        dict_members[member_id].phone = phone
    if cpf is not None:
        dict_members[member_id].cpf = cpf
    if inscription_date is not None:
        dict_members[member_id].inscription_date = datetime.datetime.strptime(inscription_date, "%Y-%m-%d %H:%M:%S")

    return {"updated":dict_members[member_id]}

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
        raise HTTPException(status_code=409, detail=f"Plan alredy exists")

    dict_planos[plan.plan_id] = plan
    print(dict_planos[plan.plan_id])
    return {"added":plan}

#Atualizar os detalhes de um plano: PUT /plans/{id}. O que será atualizado é passado nos parametros
@app.put("/plan/{plan_id}")
def update_plan(plan_id: int,
                plan_name:str | None = None,
                descr:str | None = None,
                price:int | None = None) -> dict[str, Plan]:

    if plan_id not in dict_planos:
        raise HTTPException(status_code=404, detail=f"Plan with id {plan_id} does not exist")

    if descr == price == plan_name == None:
        raise HTTPException(status_code=400, detail="Bad request: all params are null")

    if plan_name is not None:
        dict_planos[plan_id].plan_name = plan_name
    if descr is not None:
        dict_planos[plan_id].descr = descr
    if price is not None:
        dict_planos[plan_id].price = price

    return {"updated" : dict_planos[plan_id]}

#Excluir um plano: DELETE /plans/{id}
@app.delete("/plan/{plan_id}")
def update_plan(plan_id: int):
    if plan_id in dict_planos:
        del dict_planos[plan_id]
        return {"deleted":plan_id}
    raise HTTPException(status_code=404, detail=f"Plan with id {plan_id} does not exist")


#Membros de um Plano (Members in a Plan):
@app.get("/plans/all_members")
def query_members_by_plan() -> dict[int,list[Member]]:
    dic={}
    for plan in dict_planos:
        dic[plan] = []
        for member in dict_members:
            if dict_members[member].plan_id == plan:
                dic[plan].append(dict_members[member])
    return dic



#Listar todos os membros de um plano específico: GET /plans/{plan_id}/members
@app.get("/plan/{plan_id}/members")
def query_members_by_specific_plan(plan_id: int) -> list[Member]:
    if plan_id not in dict_planos:
        raise HTTPException(status_code=404, detail=f"Plan with id {plan_id} does not exist")
    plan_members = []
    for member in dict_members:
        if dict_members[member].plan_id == plan_id:
            plan_members.append(dict_members[member])
    return plan_members

#Adicionar um membro a um plano: POST /plans/{plan_id}/members
@app.put("/plan/{plan_id}/members/{member_id}") 
def get_all_members(plan_id: int, member_id:int) -> dict[str,Member]:
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(status_code=404, detail="One of the given IDs does not exisdkk")
    dict_members[member_id].plan_id = plan_id
    return {"updated": dict_members[member_id]}
    
#Remover um membro de um plano: DELETE /plans/{plan_id}/members/{member_id}
@app.delete("/plan/{plan_id}/members/{member_id}")
def delete_member(plan_id:int , member_id:int) -> dict[str,str]:
    if plan_id not in dict_planos or member_id not in dict_members:
        raise HTTPException(status_code=404, detail="One of the given IDs does not exisdkk")
    if dict_members[member_id].plan_id != plan_id:
        raise HTTPException(status_code=400, detail=f"Member {member_id} does not have the plan {dict_planos[plan_id].plan_name}")
    dict_members[member_id].plan_id = None
    return {"deleted": f"plan {dict_planos[plan_id].plan_name} from member {member_id}"}
    


#Evaluations


#Pegar todas as avaliações de um membro : GET /member/{member_id}/evaluation
@app.get("/member/{member_id}/evaluations")
def get_all_evaluations_from_member(member_id : int) -> list[Evaluation]:
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")
    return dict_members[member_id].evaluations


#Pegar uma avaliação pelo id dela
@app.get("/evaluation/{evaluation_id}")
def get_all_evaluations_from_member(evaluation_id : int) -> dict[str,Evaluation]:
    if evaluation_id not in dict_evaluations:
        raise HTTPException(status_code=404, detail=f"Evaluation with id {evaluation_id} does not exist")
    return { "evaluation" : dict_evaluations[evaluation_id].evaluations}


#Pegar a N'esima avaliacao de um membro : GET /member/{member_id}/evaluation/{evaluation_n}
@app.get("/member/{member_id}/evaluation/{evaluation_n}")
def get_all_evaluations_from_member(member_id : int, evaluation_n:int) -> dict[str,Evaluation]:
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")

    if evaluation_n >= len(dict_members[member_id].evaluations):
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not have {evaluation_n} evaluations")

    return {"evaluation" : dict_members[member_id].evaluations[evaluation_n]}

#Criar uma nova avaliacao : POST /member/{member_id}/evaluation
@app.post("/member/{member_id}/evaluation")
def create_workout_evaluation(member_id: int, evaluation:Evaluation) ->dict[str,Evaluation]:
    print("entrou")
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")
    
    if evaluation.evaluation_id in dict_evaluations:
        raise HTTPException(status_code=409, detail=f"Evaluation with same id alredy exists")

    dict_evaluations[evaluation.evaluation_id] = evaluation
    dict_members[member_id].evaluations.append(evaluation)

    return {"added":evaluation}

@app.delete("/member/{member_id}/evaluation/{evaluation_n}")
def get_all_evaluations_from_member(member_id : int, evaluation_n:int) -> dict[str,Evaluation]:
    
    if member_id not in dict_members:
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not exist")
        
    if n >= len(dict_members[member_id].evaluations):
        raise HTTPException(status_code=404, detail=f"Member with id {member_id} does not have {evaluation_n} evaluations")

    evaluation_id = dict_members[member_id].evaluations[n].evaluation_id
    dict_members[member_id].evaluations.pop(evaluation_n)
    del dict_evaluations[evaluation_id]

    return {"deleted" : f"Member {member_id} {evaluation_n}th evaluation"}

