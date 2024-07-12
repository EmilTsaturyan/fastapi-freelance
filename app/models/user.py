from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from app.db import Base



class User(Base):
        __tablename__ = 'user'

        id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
        username: Mapped[str] = mapped_column(String(length=32), nullable=False)
        email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
        hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

        projects = relationship('Project', back_populates='user')
        bids = relationship('Bid', back_populates='user')
        reviews = relationship('Review', back_populates='user')
        token = relationship('Token', back_populates='user')

