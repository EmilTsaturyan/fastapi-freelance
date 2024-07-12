from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from app.db import Base


class Token(Base):
    __tablename__ = 'token'


    token: Mapped[str] = mapped_column(String(length=320), primary_key=True, nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, unique=True)

    user = relationship('User', back_populates='token')
