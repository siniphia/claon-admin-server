import json
from datetime import date
from typing import List
from uuid import uuid4

from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, Integer, select, exists, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from claon_admin.model.enum import Role
from claon_admin.schema.conn import Base


class Contest:
    def __init__(self, year: int, title: str, name: str):
        self.year = year
        self.title = title
        self.name = name


class Certificate:
    def __init__(self, acquisition_date: date, rate: int, name: str):
        self.acquisition_date = acquisition_date
        self.rate = rate
        self.name = name


class Career:
    def __init__(self, start_date: date, end_date: date, name: str):
        self.start_date = start_date
        self.end_date = end_date
        self.name = name


class User(Base):
    __tablename__ = 'tb_user'
    id = Column(String(length=255), primary_key=True, default=str(uuid4()))
    nickname = Column(String(length=20), nullable=False, unique=True)
    profile_img = Column(String(length=255), nullable=False)
    sns = Column(String(length=500), nullable=False, unique=True)
    email = Column(String(length=500), unique=True)
    instagram_name = Column(String(length=255), unique=True)
    role = Column(Enum(Role), nullable=False)


class Lector(Base):
    __tablename__ = 'tb_lector'
    id = Column(String(length=255), primary_key=True, default=str(uuid4()))
    user_id = Column(String(length=255), ForeignKey("tb_user.id"), unique=True)
    user = relationship("User")
    is_setter = Column(Boolean, default=False, nullable=False)
    total_experience = Column(Integer, nullable=False, default=0)
    _contest = Column(Text)
    _certificate = Column(Text)
    _career = Column(Text)
    approved_files = relationship("LectorApprovedFile", back_populates="lector")
    approved = Column(Boolean, default=False, nullable=False)

    @property
    def contest(self):
        return json.loads(self._contest)

    @contest.setter
    def contest(self, values: List[Contest]):
        self._contest = json.dumps([value.__dict__ for value in values], default=str)

    @property
    def certificate(self):
        return json.loads(self._certificate)

    @certificate.setter
    def certificate(self, values: List[Certificate]):
        self._certificate = json.dumps([value.__dict__ for value in values], default=str)

    @property
    def career(self):
        return json.loads(self._career)

    @career.setter
    def career(self, values: List[Career]):
        self._career = json.dumps([value.__dict__ for value in values], default=str)


class LectorApprovedFile(Base):
    __tablename__ = 'tb_lector_approved_file'
    id = Column(String(length=255), primary_key=True, default=str(uuid4()))
    lector_id = Column(String(length=255), ForeignKey('tb_lector.id'))
    lector = relationship("Lector")
    url = Column(String(length=255))


class UserRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, user_id: str):
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().one_or_none()

    @staticmethod
    async def find_by_nickname(session: AsyncSession, nickname: str):
        result = await session.execute(select(User).where(User.nickname == nickname))
        return result.scalars().one_or_none()

    @staticmethod
    async def exist_by_id(session: AsyncSession, user_id: str):
        result = await session.execute(select(exists().where(User.id == user_id)))
        return result.scalar()

    @staticmethod
    async def exist_by_nickname(session: AsyncSession, nickname: str):
        result = await session.execute(select(exists().where(User.nickname == nickname)))
        return result.scalar()

    @staticmethod
    async def save(session: AsyncSession, user: User):
        session.add(user)
        await session.flush()
        return user


class LectorRepository:
    @staticmethod
    async def save(session: AsyncSession, lector: Lector):
        session.add(lector)
        await session.flush()
        return lector


class LectorApprovedFileRepository:
    @staticmethod
    async def save(session: AsyncSession, approved_files: LectorApprovedFile):
        session.add(approved_files)
        await session.flush()
        return approved_files
