from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

class TransactionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute_with_transaction(self, func, *args, **kwargs):
        async with self.session.begin():
            try:
                return await func(*args, **kwargs)
            except SQLAlchemyError as e:
                await self.session.rollback()
                print(f"Ошибка транзакции: {e}")
                raise HTTPException(status_code=500, detail="Transaction error")
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
            finally:
                await self.session.close()