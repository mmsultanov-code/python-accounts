from decimal import ROUND_DOWN, Decimal
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from app.models.account import Account, IncomingFunds
from datetime import datetime
from fastapi import HTTPException
from typing import Optional
from app.schemas.account import IncomingFundCreate
from app.models.user import User

class AccountService:

    async def create_account(session: AsyncSession, user_id: int):
        """
        Create a new account with the given user ID and session.

        Args:
            user_id (int): The ID of the user associated with the account.
            session (AsyncSession): The async session object for database operations.

        Returns:
            Account: The newly created account object.

        Raises:
            HTTPException: If there is an error while creating the account.
        """
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

    async def get_account(session: AsyncSession, account_id: int):
        """
        Get an account by its account ID.

        Parameters:
        - account_id (int): The ID of the account to retrieve.
        - session (AsyncSession): The database session to use for the query.

        Returns:
        - Account: The account object corresponding to the given account ID.

        Raises:
        - HTTPException: If the account with the given ID is not found.
        """
        result = await session.execute(select(Account).filter_by(account_id=account_id))
        account = result.scalars().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def make_naive(dt: datetime) -> datetime:
        """
        Converts a datetime object to a naive datetime object by removing the timezone information.

        Args:
            dt (datetime): The datetime object to be converted.

        Returns:
            datetime: A naive datetime object without timezone information.
        """
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt

    async def get_account_balance(session: AsyncSession, account_id: int, target_datetime: Optional[datetime] = None):
        """
        Retrieves the account balance for the specified account ID.
        Args:
            account_id (int): The ID of the account.
            session (AsyncSession): The async session object for database operations.
            target_datetime (Optional[datetime], optional): The target datetime to calculate the future balance. Defaults to None.
        Returns:
            float: The account balance.
        Raises:
            HTTPException: If the account is not found or if there is an internal server error.
        """
        try:
            # Получение текущего баланса
            result = await session.execute(select(Account).where(Account.account_id == account_id))
            account = result.scalars().first()

            if not account:
                raise HTTPException(status_code=404, detail="Account not found")

            print(account.balance)
            current_balance = account.balance

            # Если datetime не указан, возвращаем текущий баланс
            if not target_datetime:
                return current_balance

            # Приводим target_datetime к наивному datetime
            target_datetime = AccountService.make_naive(target_datetime)

            # Получение всех средств, которые будут урегулированы до указанного времени
            stmt = select(IncomingFunds)\
                .filter(IncomingFunds.account_id == account_id)
            result = await session.execute(stmt)
            incoming_funds = result.scalars().all()

            future_balance = 0
            for fund in incoming_funds:
                future_balance += fund.amount

            return future_balance
        except HTTPException as e:
            raise e
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка при получении баланса аккаунта: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def process_settlement(session: AsyncSession, fund_id: int):
        """
        Process settlement for a given fund ID.
        Parameters:
        - fund_id (int): The ID of the fund to process settlement for.
        - session (AsyncSession): The asynchronous session object for database operations.
        Raises:
        - HTTPException: If the fund with the given ID is not found.
        Returns:
        - None
        """
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

    def calculate_new_balance(amount, funds):
        new_balance = 0
        if amount < 0:
            new_balance -= round(abs(Decimal(amount)))
        elif amount > 0:
            new_balance += Decimal(amount)

        for fund in funds:
            if fund.amount < 0:
                new_balance -= round(abs(Decimal(fund.amount)))
            elif fund.amount > 0:
                new_balance += Decimal(fund.amount)

        return new_balance

    async def add_incoming_fund(session: AsyncSession, fund_data: IncomingFundCreate):
        """
        Adds a new record of incoming funds to the database and updates the account balance.

        Args:
            fund_data (IncomingFundCreate): The data for the incoming funds.
            session (AsyncSession): The database session.

        Returns:
            IncomingFunds: The newly created incoming funds record.

        Raises:
            HTTPException: If there is an error adding the incoming funds or updating the account balance.
        """
        try:
            # Внешняя транзакция
            async with session.begin():
                try:
                    # Приведение даты к наивному datetime
                    target_datetime = AccountService.make_naive(fund_data.settlement_date)

                    # Получение аккаунта
                    account = await session.execute(
                        select(Account).where(Account.account_id == fund_data.account_id)
                    )
                    account = account.scalars().first()

                    if not account:
                        raise HTTPException(status_code=404, detail="Account not found")
                    
                    funds = await session.execute(select(IncomingFunds).filter_by(account_id=fund_data.account_id))
                    funds = funds.scalars().all()

                    new_balance = AccountService.calculate_new_balance(fund_data.amount, funds)

                    # Обновление баланса аккаунта
                    await session.execute(
                        update(Account)
                        .where(Account.account_id == fund_data.account_id)
                        .values(balance=Decimal(new_balance))
                    )

                    # Создание новой записи о входящих средствах
                    new_fund = IncomingFunds(
                        account_id=fund_data.account_id,
                        amount=fund_data.amount,
                        settlement_date=target_datetime
                    )

                    # Вложенная транзакция для добавления новой записи
                    async with session.begin_nested():
                        session.add(new_fund)

                    # Фиксация изменений
                    await session.flush()
                    await session.refresh(new_fund)

                    return new_fund

                except Exception as e:
                    # Логирование ошибки
                    print(f"Ошибка при добавлении входящих средств: {e}")
                    raise HTTPException(status_code=500, detail=str(e))

        except Exception as e:
            # Логирование общей ошибки
            print(f"Ошибка в методе: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def get_user_by_id(session: AsyncSession, user_id: int):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.
            session (AsyncSession): The database session.

        Returns:
            User: The user object.

        Raises:
            HTTPException: If the user is not found.
        """
        try:
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().first()
            return user
        except Exception as e:
            print(f"Ошибка при получении пользователя по ID: {e}")
            raise HTTPException(status_code=404, detail="User not found")