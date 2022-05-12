import uuid
from datetime import date

from pydantic import BaseModel

from app.db.models import UserDB
from app.enums.documents_enum import DocumentsEnum
from app.enums.gender_enum import GenderEnum


class User(BaseModel):
    id: uuid.UUID
    first_name: str
    middle_name: str | None = None
    last_name: str
    gender: GenderEnum
    document_type: DocumentsEnum
    document_number: str
    date_birth: date

    class Config:
        orm_mode = True

