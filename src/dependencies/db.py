from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД из request.state."""
    db_session = request.state.db  # Получаем сессию из request.state
    try:
        yield db_session  # Возвращаем сессию в качестве контекста
    except Exception:
        await db_session.rollback()  # Откат при ошибке
        raise
    finally:
        # Сессия будет закрыта в middleware после запроса
        pass