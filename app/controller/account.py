from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database import get_async_session
from app.schemas.account import AccountBalanceRequest, AccountCreate, IncomingFundCreate, AccountCreateResponse, AccountBalanceResponse, IncomingFundCreateResponse, SettlementResponse
from app.services.account import AccountService
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/auth",
)

# Маршрут для создания нового аккаунта
@router.post("/accounts/", response_model=AccountCreateResponse)
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
        user = await AccountService.get_user_by_id(session, account_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        account = await AccountService.create_account(session, account_data.user_id)
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

# Маршрут для получения баланса счета
@router.post("/account/balance", response_model=AccountBalanceResponse)
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
    balance = await AccountService.get_account_balance(session, request.account_id)
    return {"account_id": request.account_id, "balance": balance}

# Маршрут для добавления входящих средств
@router.post("/incoming-fund/", response_model=IncomingFundCreateResponse)
async def create_incoming_fund(fund_data: IncomingFundCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create an incoming fund.

    Parameters:
    - fund_data: The data for creating the incoming fund.
    - session: The async session for database operations.

    Returns:
    - The created incoming fund.
    """
    try:
        fund = await AccountService.add_incoming_fund(session, fund_data)
        return fund
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для обработки урегулирования средств
@router.post("/settlement/{fund_id}", response_model=SettlementResponse)
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
    await AccountService.process_settlement(session, fund_id)
    return {"message": "Settlement processed"}