from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import BaseModel

Base = declarative_base()

class User(Base, BaseModel):
    __tablename__ = "user"
    
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    admin = relationship("Admin", uselist=False, back_populates="user", cascade="all, delete, delete-orphan")
    customer = relationship("Customer", uselist=False, back_populates="user", cascade="all, delete, delete-orphan")

class Admin(Base, BaseModel):
    __tablename__ = "admin"
    
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="admin")

class Customer(Base, BaseModel):
    __tablename__ = "customer"
    
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="customer")
    
class Investment(Base, BaseModel):
    __tablename__ = "investment"
    
    title = Column(String, nullable=False)
    appreciation_amount = Column(Integer, nullable=False)
    appreciation_duration = Column(Integer, nullable=False)
    lock_period = Column(Integer, nullable=False)
    withdrawal_cost = Column(Integer, nullable=False)