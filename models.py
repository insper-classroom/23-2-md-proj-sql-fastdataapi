from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base


class Plan(Base):
    __tablename__ = "plans"

    plan_id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )
    plan_name = Column(String(100), unique=True, index=True, nullable=False)
    descr = Column(String(500), index=True, nullable=False)
    price = Column(Numeric(precision=10, scale=2), index=True, nullable=False)

    # Defina o relacionamento com a classe Member
    members = relationship("Member", back_populates="plan")


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

    # Defina o relacionamento com a classe Plan
    plan = relationship("Plan", back_populates="members")
