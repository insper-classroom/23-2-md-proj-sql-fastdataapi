from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Member(Base):
    __tablename__ = "members"

    member_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    name = Column(String(100), index=True, nullable=False)
    birth_date = Column(DateTime, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(50), unique=True, index=True, nullable=True)
    cpf = Column(String(50), unique=True, index=True, nullable=False)
    incription_date = Column(DateTime, index=True, nullable=False)

    plans = relationship("Plan", back_populates="plan_owner")
    evaluations = relationship(
        "Evaluation",
        back_populates="evaluation_owner",
        foreign_keys="[Evaluation.member_id, Evaluation.evaluation_owner_id]",
    )


class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    plan_name = Column(String(100), unique=True, index=True, nullable=False)
    descr = Column(String(500), index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    plan_owner_id = Column(Integer, ForeignKey("members.member_id"))

    plan_owner = relationship("Member", foreign_keys=[plan_owner_id])


class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id = Column(Integer, primary_key=True, index=True)
    evaluation_date = Column(DateTime, index=True, nullable=False)
    weight = Column(Float, index=True, nullable=False)
    height = Column(Float, index=True, nullable=False)
    fat_percentage = Column(Float, index=True, nullable=True)
    observation = Column(String(500), index=True, nullable=True)
    member_id = Column(Integer, ForeignKey("members.member_id"))
    evaluation_owner_id = Column(Integer, ForeignKey("members.member_id"))

    evaluation_owner = relationship("Member", back_populates="evaluations")
