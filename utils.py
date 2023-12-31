from fastapi import HTTPException
from sqlalchemy.orm import Session
import datetime
import models, schemas


def db_get_members(db: Session, id: int | None = None):
    if id is not None:
        return db.query(models.Member).filter(models.Member.member_id == id).first()
    return db.query(models.Member).all()


def db_get_members_name(db: Session, name: str):
    return db.query(models.Member).filter(models.Member.name == name).all()


def db_create_member(db: Session, member: schemas.MemberCreate):
    try:
        db_member = models.Member(
            name=member.name,
            birth_date=member.birth_date,
            email=member.email,
            phone=member.phone,
            cpf=member.cpf,
            inscription_date=member.inscription_date,
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member
    except:
        raise HTTPException(status_code=409, detail="Cannot create member")


def db_update_member(
    db: Session,
    member_id: int,
    name: str | None = None,
    birth_date: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    cpf: str | None = None,
    inscription_date: str | None = None,
):
    member = db_get_members(db, id=member_id)
    if name is not None:
        member.name = name
    if birth_date is not None:
        member.birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S")
    if email is not None:
        member.email = email
    if phone is not None:
        member.phone = phone
    if cpf is not None:
        member.cpf = cpf
    if inscription_date is not None:
        member
        inscription_date = datetime.datetime.strptime(
            inscription_date, "%Y-%m-%d %H:%M:%S"
        )
    db.commit()
    return member


def db_delete_members(db: Session, id: int):
    db.query(models.Member).filter(models.Member.member_id == id).delete()
    db.commit()


def db_get_plan(db: Session, id: int | None = None):
    if id is not None:
        return db.query(models.Plan).filter(models.Plan.plan_id == id).first()
    return db.query(models.Plan).all()

def db_get_plan_name(db: Session, name: str):
    return db.query(models.Plan).filter(models.Plan.plan_name == name).all()

def db_post_plan(db: Session, plan: schemas.Plan):
    try:
        db_plan = models.Plan(
            plan_name=plan.plan_name,
            descr=plan.descr,
            price=plan.price,
        )
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        return db_plan
    except:
        raise HTTPException(status_code=409, detail="Cannot create member")


def db_update_plan(
    db: Session,
    plan_id: int,
    plan_name: str | None = None,
    descr: str | None = None,
    price: float | None = None,
):
    plan = db_get_plan(db, id=plan_id)
    if plan_name is not None:
        plan.plan_name = plan_name
    if descr is not None:
        plan.descr = descr
    if plan_name is not None:
        plan.price = price

    db.commit()
    return plan


def db_delete_plan(db: Session, id: int):
    db.query(models.Plan).filter(models.Plan.plan_id == id).delete()
    db.commit()


def db_add_member_to_plan(db: Session, member_id: int, plan_id: int):
    membro = db_get_members(db, member_id)
    membro.plan_id = plan_id
    db.commit()
    return membro

def db_remove_plan_from_member(db: Session, member_id: int):
    membro = db_get_members(db, member_id)
    membro.plan_id = None
    db.commit()
    return membro
