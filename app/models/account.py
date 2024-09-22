from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, validates

from app.common.database import Base

class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    balance = Column(DECIMAL(18, 2), default=0)

    owner = relationship("User", back_populates="accounts")
    incoming_funds = relationship("IncomingFunds", back_populates="accounts")


class IncomingFunds(Base):
    __tablename__ = "incoming_fund"

    fund_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.account_id"))
    amount = Column(DECIMAL(18, 2), nullable=False)
    settlement_date = Column(DateTime, nullable=False)

    accounts = relationship("Account", back_populates="incoming_funds")