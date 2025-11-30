from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, String, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TokenBalance(Base):
    __tablename__ = "token_balances"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    balance_btn = Column(BigInteger, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="token_balance")


class TokenTransaction(Base):
    __tablename__ = "token_transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    delta_btn = Column(BigInteger, nullable=False)
    type = Column(String(30), nullable=False)
    source = Column(String(50), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
