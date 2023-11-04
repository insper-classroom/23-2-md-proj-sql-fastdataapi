from sqlalchemy.orm import session

from . import models, schemas

def db_get_members(db : Session, id:int | None = None):
    if id is not None:
        return db.query(models.Member).filter(models.Member.member_id == id).first()
    return db.query(models.Member).all()


def db_create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(member_id=member.member_id,
                              name = member.name,
                              email = member.email,
                              phone = member.phone,
                              cpf = member.cpf,
                              inscription_date = member.inscription_date,
                              plan_id = member.plan_id)
    db.add(db_member)
    db.commit()
    db.refresh(db_user)
    return db_user

def db_update_member(db : Session,
                     member_id: int,
                     name:str | None = None,
                     birth_date:str | None = None,
                     email: str | None = None, 
                     phone: str | None = None,
                     cpf: str | None = None,
                     inscription_date: str | None = None):

    member = db.query(models.Member).filter(models.Member.member_id == id).first()
    if name is not None:
        member.name = name
    if birth_date is not None:
        member.birth_date = datetime.datetime.strptime(
            birth_date, "%Y-%m-%d %H:%M:%S")
    if email is not None:
        member.email = email
    if phone is not None:
        member.phone = phone
    if cpf is not None:
        member.cpf = cpf
    if inscription_date is not None:
        member;inscription_date = datetime.datetime.strptime(
            inscription_date, "%Y-%m-%d %H:%M:%S")
    db.commit()
    return member

def db_delete_members(db : Session, id:int):
    db.query(models.Member).filter(models.Member.member_id == id).delete()
    db.commit()

def db_get_plan(db: Session, id: int | None=None):
    if id is not None:
        return db.query(models.Plan).filter(models.Member.member_id == id).first()
    return db.query(models.Member).all()

def db_post_plan(db: Session, plan: schemas.plan):
    db_plan = models.Member(plan_id=plan.plan_id,
                            plan_name = plan.plan_name,
                            descr = plan.descr,
                            price = plan.price)
    db.add(db_plan)
    db.commit()
    db.refresh(db_user)
    return db_user

def db_update_plan(db: Session,
                   plan_id: int,
                   plan_name: str | None=None,
                   descr: str | None=None,
                   price: float | None=None):
    plan = db.query(models.plan).filter(models.Member.member_id == id).first()
    if plan_name is not None:
        plan.plan_name = plan_name
    if descr is not None:
        plan.descr = descr
    if phone is not None:
        plan.price = price
    db.add(plan)
    db.commit()
    db.refresh(db_user)

def db_remove_plan(db: Session, id:int):
    db.query(models.Plan).filter(models.Plan.member_id == id).delete()
    db.commit()

def db_get_evaluation(db: Session, id: int):
    if id is not None:
        return db.query(models.Evaluation).filter(models.Evaluation.evaluation_id == id).first()
    return db.query(models.Evaluation).all()

def db_get_evaluation(db: Session, id: int):
    if id is not None:
        return db.query(models.Evaluation).filter(models.Evaluation.evaluation_owner_id == id).all()
    return db.query(models.Member).all()

def db_create_workout_evaluation(db: Session, evaluation : Evaluation):
    db_eval = models.Evaluation(evaluation_id = evaluation.evaluation_id,
                              evaluation_owner_id = evaluation.evaluation_owner_id,
                              evaluation_date = evaluation.evaluation_date,
                              weight = evaluation.weight,
                              height = evaluation.height,
                              fat_percentage = evaluation.fat_percentage,
                              observation = evaluation.observation)
    db.add(db_eval)
    db.commit()
    db.refresh(db_eval)
    return db_eval
