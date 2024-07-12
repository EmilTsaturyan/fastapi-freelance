from pydantic import BaseModel


class ReviewBase(BaseModel):
    rating: int
    comment: str


class ReviewCreate(ReviewBase):
    project_id: int


class ReviewUpdate(ReviewBase):
    pass


class ReviewUpdatePartial(ReviewBase):
    rating: int | None = None
    comment: str | None = None


class Review(ReviewCreate):
    id: int

    class Config:
        from_attributes = True
