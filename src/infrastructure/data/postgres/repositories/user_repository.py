from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.application.auth.interfaces.repo import IUserRepository
from src.infrastructure.data.postgres.models.user import User as ORMUser  
from src.domain.auth.entities.user import User as DomainUser

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: DomainUser) -> None:
        orm_user = ORMUser(
            id=str(user.id),
            email=user.email,
            password_hash=user.password_hash,
            fio=user.fio,
            org=user.org,
            created_at=user.created_at
        )
        self.session.add(orm_user)
        await self.session.commit()

    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        stmt = select(ORMUser).where(ORMUser.email == email.lower())
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        if not orm_user:
            return None
        return DomainUser(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            fio=orm_user.fio,
            org=orm_user.org,
            created_at=orm_user.created_at
        )

    async def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        stmt = select(ORMUser).where(ORMUser.id == user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        if not orm_user:
            return None
        return DomainUser(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            fio=orm_user.fio,
            org=orm_user.org,
            created_at=orm_user.created_at
        )