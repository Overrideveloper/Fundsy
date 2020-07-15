from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import BaseModel, TransactionType

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
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete, delete-orphan")
    customer_investments = relationship("CustomerInvestment", back_populates="customer", cascade="all, delete, delete-orphan")

class Investment(Base, BaseModel):
    __tablename__ = "investment"
    
    title = Column(String, nullable=False)
    appreciation_amount = Column(Integer, nullable=False)
    appreciation_duration = Column(Integer, nullable=False)
    lock_period = Column(Integer, nullable=False)
    withdrawal_cost = Column(Integer, nullable=False)
    customer_investments = relationship("CustomerInvestment", back_populates="investment", cascade="all, delete, delete-orphan")
    
class CustomerInvestment(Base, BaseModel):
    __tablename__ = "customer_investment"

    title = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    investment_id = Column(Integer, ForeignKey("investment.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    investment = relationship("Investment", back_populates="customer_investments")
    customer = relationship("Customer", back_populates="customer_investments")
    transactions = relationship("Transaction", back_populates="customer_investment", cascade="all, delete, delete-orphan")
    
class Transaction(Base, BaseModel):
    __tablename__ = "transaction"
    
    amount = Column(Numeric, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    customer_investment_id = Column(Integer, ForeignKey("customer_investment.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer_investment = relationship("CustomerInvestment", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")
