from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database import get_async_session
from app.schemas.account import AccountBalanceRequest, AccountCreate, IncomingFundCreate
from app.services.account import create_account, get_account_balance, process_settlement, get_user_by_id, add_incoming_fund
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/auth",
)

# Маршрут для получения баланса счета
@router.post("/account/balance")
async def account_balance(request: AccountBalanceRequest, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve the account balance for a given account ID.

    Parameters:
    - request (AccountBalanceRequest): The request object containing the account ID and datetime.
    - session (AsyncSession, optional): The async session to use for the database transaction. Defaults to None.

    Returns:
    - dict: A dictionary containing the account ID and balance.

    Raises:
    - HTTPException: If there is a transaction error or internal server error.
    """
    try:
        async with session.begin():
            balance = await get_account_balance(request.account_id, session, request.datetime)
        return {"account_id": request.account_id, "balance": balance}
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка транзакции: {e}")
        raise HTTPException(status_code=500, detail="Transaction error")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Маршрут для добавления входящих средств
@router.post("/incoming-fund/")
async def create_incoming_fund(fund_data: IncomingFundCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create an incoming fund.

    Parameters:
    - fund_data: The data for creating the incoming fund.
    - session: The async session for database operations.

    Returns:
    - The created incoming fund.
    """
    fund = await add_incoming_fund(fund_data, session)
    return fund


# Маршрут для обработки урегулирования средств
@router.post("/settlement/{fund_id}")
async def settlement(fund_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Process settlement for a given fund ID.

    Parameters:
    - fund_id (int): The ID of the fund to process settlement for.
    - session (AsyncSession, optional): The async session to use for the database transaction. Defaults to `Depends(get_async_session)`.

    Returns:
    - dict: A dictionary containing the message "Settlement processed".

    Raises:
    - HTTPException: If there is a transaction error or an internal server error occurs.
    """
    try:
        async with session.begin():
            await process_settlement(fund_id, session)
        return {"message": "Settlement processed"}
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка транзакции: {e}")
        raise HTTPException(status_code=500, detail="Transaction error")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/accounts/", response_model=AccountCreate)
async def create_new_account(account_data: AccountCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new account for a user.
    Args:
        account_data (AccountCreate): The account data for the new account.
        session (AsyncSession, optional): The async session to use for the database transaction. Defaults to Depends(get_async_session).
    Returns:
        Account: The newly created account.
    Raises:
        HTTPException: If the user is not found or if there is an error during the transaction.
    """
    try:
        # Проверяем, существует ли пользователь
        user = await get_user_by_id(account_data.user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        account = await create_account(user_id=account_data.user_id, session=session)
        return account

    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Ошибка транзакции: {e}")
        raise HTTPException(status_code=500, detail="Transaction error")

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        await session.close()