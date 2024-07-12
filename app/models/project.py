from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from app.db import Base



class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[int] = mapped_column(Integer, nullable=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='projects')
    bids = relationship('Bid', back_populates='project', cascade='all, delete')
    reviews = relationship('Review', back_populates='project', cascade='all, delete')