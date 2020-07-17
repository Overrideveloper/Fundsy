from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import BaseModel, TransactionType

Base = declarative_base()

class User(Base, BaseModel):
    __tablename__ = "user"
    
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    admin = relationship("Admin", uselist=False, back_populates="user", passive_deletes=True)
    customer = relationship("Customer", uselist=False, back_populates="user", passive_deletes=True)

class Admin(Base, BaseModel):
    __tablename__ = "admin"
    
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="admin")

class Customer(Base, BaseModel):
    __tablename__ = "customer"
    
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="customer")
    transactions = relationship("Transaction", back_populates="customer", passive_deletes=True)
    customer_investments = relationship("CustomerInvestment", back_populates="customer", passive_deletes=True)

class Investment(Base, BaseModel):
    __tablename__ = "investment"
    
    title = Column(String, nullable=False)
    appreciation_amount = Column(Integer, nullable=False)
    appreciation_duration = Column(Integer, nullable=False)
    lock_period = Column(Integer, nullable=False)
    withdrawal_cost = Column(Integer, nullable=False)
    customer_investments = relationship("CustomerInvestment", back_populates="investment")
    
class CustomerInvestment(Base, BaseModel):
    __tablename__ = "customer_investment"

    title = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    appreciation = Column(Integer, nullable=False, default=0)
    investment_id = Column(Integer, ForeignKey("investment.id"))
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"))
    investment = relationship("Investment", back_populates="customer_investments")
    customer = relationship("Customer", back_populates="customer_investments")
    transactions = relationship("Transaction", back_populates="customer_investment", passive_deletes=True)
    appreciation_logs = relationship("AppreciationLog", back_populates="customer_investment", passive_deletes=True)
    
class Transaction(Base, BaseModel):
    __tablename__ = "transaction"
    
    amount = Column(Integer, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String, nullable=False)
    customer_investment_id = Column(Integer, ForeignKey("customer_investment.id", ondelete="CASCADE"))
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"))
    customer_investment = relationship("CustomerInvestment", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")

class AppreciationLog(Base, BaseModel):
    __tablename__ = "appreciation_log"
    
    old_amount = Column(Integer, nullable=False)
    new_amount = Column(Integer, nullable=False)
    customer_investment_id = Column(Integer, ForeignKey("customer_investment.id", ondelete="CASCADE"))
    customer_investment = relationship("CustomerInvestment", back_populates="appreciation_logs")
