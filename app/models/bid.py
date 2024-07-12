from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from app.db import Base



class Bid(Base):
    __tablename__ = 'bid'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    cover_letter: Mapped[str] = mapped_column(Text, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id', ondelete='CASCADE'))
    bidder_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    project = relationship('Project', back_populates='bids')
    user = relationship('User', back_populates='bids')

