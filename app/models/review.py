from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from app.db import Base



class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='reviews')
    project = relationship('Project', back_populates='reviews')