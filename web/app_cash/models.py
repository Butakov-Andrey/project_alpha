import enum
import uuid

import postgres_db
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

Base = postgres_db.Base


class CategoryTypes(enum.Enum):
    income = "income"
    expense = "expense"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    balance = Column(Integer, CheckConstraint("balance >= 0"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # relationships
    transactions = relationship("Transaction", back_populates="wallet")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    type = Column(Enum(CategoryTypes), nullable=False)
    # relationships
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    value = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    wallet_id = Column(String, ForeignKey("wallets.id"), nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    # relationships
    wallet = relationship("Wallet", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
