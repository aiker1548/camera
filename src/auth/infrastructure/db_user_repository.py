from typing import Optional
from sqlalchemy.orm import Session
from src.auth.domain import User as DomainUser
from src.auth.repositories import IUserRepository
from src.shared.models import User as ORMUser  # SQLAlchemy model
from src.shared.database import get_session


class UserRepository(IUserRepository):
    def __init__(self, session: Session = None):
        self.session = session or get_session()

    def add(self, user: DomainUser) -> None:
        orm_user = ORMUser(
            id=str(user.id),
            email=user.email,
            password_hash=user.password_hash,
            fio=user.fio,
            org=user.org,
            created_at=user.created_at
        )
        self.session.add(orm_user)
        self.session.commit()

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        orm_user = (
            self.session.query(ORMUser)
            .filter(ORMUser.email == email.lower())
            .first()
        )
        if not orm_user:
            return None
        return DomainUser(
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            fio=orm_user.fio,
            org=orm_user.org
        )

    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        orm_user = self.session.query(ORMUser).get(user_id)
        if not orm_user:
            return None
        return DomainUser(
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            fio=orm_user.fio,
            org=orm_user.org
        )
