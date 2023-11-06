from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    plan_name = Column(String(100), unique=True, index=True, nullable=False)
    descr = Column(String(500), index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)

    # plan_owner_id = Column(Integer, ForeignKey("members.member_id"))

    # membro = relationship("Member", back_populates="plano")


class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id = Column(Integer, primary_key=True, index=True)
    evaluation_date = Column(DateTime, index=False, nullable=False)
    weight = Column(Float, index=False, nullable=False)
    height = Column(Float, index=False, nullable=False)
    fat_percentage = Column(Float, index=True, nullable=True)
    observation = Column(String(500), index=True, nullable=True)

    member_id = Column(Integer, ForeignKey("members.member_id"))

    # evaluation_owner_id = Column(Integer, ForeignKey("members.member_id"))

    # evaluation_owner = relationship("Member", back_populates="evaluations")


class Member(Base):
    __tablename__ = "members"

    member_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    name = Column(String(100), index=True, nullable=False)
    birth_date = Column(DateTime, index=True, nullable=False)
    email = Column(String(100), unique=True, index=False, nullable=False)
    phone = Column(String(50), unique=True, index=False, nullable=True)
    cpf = Column(String(50), unique=True, index=False, nullable=False)
    inscription_date = Column(DateTime, index=False, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.plan_id"), nullable=True)

    # plans = relationship("Plan", back_populates="plan_owner")
    # plano = relationship("Plan", back_populates="members")

    # evaluations = relationship(
    #     "Evaluation",
    #     back_populates="evaluation_owner",
    # )

    evaluations = relationship("Evaluation", foreign_keys=[Evaluation.member_id])
