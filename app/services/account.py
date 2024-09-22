from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from app.models.account import Account, IncomingFunds
from datetime import datetime
from fastapi import HTTPException
from typing import Optional
from app.schemas.account import AccountBalanceRequest, IncomingFundCreate
from app.models.user import User


async def create_account(user_id: int, session: AsyncSession):
    try:
        # Создаем новый аккаунт с балансом по умолчанию
        new_account = Account(user_id=user_id, balance=0)
        session.add(new_account)
        await session.commit()
        await session.refresh(new_account)  # Обновляем объект после сохранения
        return new_account
    except Exception as e:
        # Логирование ошибки
        print(f"Ошибка при создании аккаунта: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_account(account_id: int, session: AsyncSession):
    result = await session.execute(select(Account).filter_by(account_id=account_id))
    account = result.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

def make_naive(dt: datetime) -> datetime:
    """Удаляет информацию о временной зоне, если она присутствует"""
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

async def get_account_balance(account_id: int, session: AsyncSession, target_datetime: Optional[datetime] = None):
    try:
        # Получение текущего баланса
        result = await session.execute(select(Account).filter_by(account_id=account_id))
        account = result.scalars().first()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        current_balance = account.balance

        # Если datetime не указан, возвращаем текущий баланс
        if not target_datetime:
            return current_balance

        # Приводим target_datetime к наивному datetime
        target_datetime = make_naive(target_datetime)

        # Получение всех средств, которые будут урегулированы до указанного времени
        stmt = select(IncomingFunds)\
            .filter(IncomingFunds.account_id == account_id)\
            .filter(IncomingFunds.settlement_date <= target_datetime)
        result = await session.execute(stmt)
        incoming_funds = result.scalars().all()

        future_balance = current_balance
        for fund in incoming_funds:
            future_balance += fund.amount

        return future_balance
    except HTTPException as e:
        raise e
    except Exception as e:
        # Логирование ошибки
        print(f"Ошибка при получении баланса аккаунта: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_settlement(fund_id: int, session: AsyncSession):
    # Получение входящих средств по ID
    result = await session.execute(select(IncomingFunds).filter_by(fund_id=fund_id))
    fund = result.scalars().first()

    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Транзакция: добавляем средства к счету и удаляем запись о входящих средствах
    async with session.begin_nested():
        await session.execute(
            update(Account)
            .where(Account.account_id == fund.account_id)
            .values(balance=Account.balance + fund.amount)
        )
        await session.execute(
            delete(IncomingFunds).where(IncomingFunds.fund_id == fund_id)
        )
    await session.commit()

async def add_incoming_fund(fund_data: IncomingFundCreate, session: AsyncSession):
    try:
        # Создаем новую запись о входящих средствах
        target_datetime = make_naive(fund_data.settlement_date)
        new_fund = IncomingFunds(account_id=fund_data.account_id, amount=fund_data.amount, settlement_date=target_datetime)
        session.add(new_fund)
        await session.commit()
        await session.refresh(new_fund)
        return new_fund
    except Exception as e:
        # Логирование ошибки
        print(f"Ошибка при добавлении входящих средств: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def get_user_by_id(user_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        return user
    except Exception as e:
        print(f"Ошибка при получении пользователя по ID: {e}")
        raise HTTPException(status_code=404, detail="User not found")