from pydantic import BaseModel



class BidBase(BaseModel):
    cover_letter: str
    amount: int


class BidCreate(BidBase):
    project_id: int


class BidUpdate(BidBase):
    pass


class BidUpdatePartial(BidBase):
    cover_letter: str | None = None
    amount: int | None = None


class Bid(BidCreate):
    id: int
    
    class Config:
        from_attributes = True

