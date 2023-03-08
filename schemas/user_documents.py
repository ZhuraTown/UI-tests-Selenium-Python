from pydantic import BaseModel


class UserDocument(BaseModel):
    id: int
    title: str
    owner: int
