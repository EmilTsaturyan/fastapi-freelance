from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: str
    budget: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectUpdatePartial(ProjectBase):
    title: str | None = None
    description: str | None = None
    budget: int | None = None
    

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True

