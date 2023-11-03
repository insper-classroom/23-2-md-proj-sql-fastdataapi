from sqlalchemy.orm import session

from . import models, schemas

def db_get_members(db : Session, Id:int | None = None):
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

def db_update_member(member_id: int,
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

def db_delete_members(db : Session, Id:int | None = None):
    db.query(models.Member).filter(models.Member.member_id == id).delete()
    db.commit()
