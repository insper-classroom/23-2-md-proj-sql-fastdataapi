from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    plan_name = Column(String, unique=True, index=True, nullable=False)
    descr = Column(String, index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)

    plan_owner = relationship("Member", back_populates="plans")


class Evaluation(Base):
    __tablename__ = "evaluations"

    evaluation_id = Column(Integer, primary_key=True, index=True)
    evaluation_date = Column(DateTime, index=True, nullable=False)
    weight = Column(Float, index=True, nullable=False)
    height = Column(Float, index=True, nullable=False)
    fat_percentage = Column(Float, index=True, nullable=True)
    observation = Column(String, index=True, nullable=True)
    member_id = Column(Integer, ForeignKey("members.member_id"))

    evaluation_owner = relationship("Member", back_populates="evaluations")


class Member(Base):
    __tablename__ = "members"

    member_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    name = Column(String, index=True, nullable=False)
    birth_date = Column(DateTime, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    cpf = Column(String, unique=True, index=True, nullable=False)
    incription_date = Column(DateTime, index=True, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.plan_id"))

    plans = relationship("Plan", back_populates="plan_owner")
    evaluations = relationship("Evaluation", back_populates="evaluation_owner")
