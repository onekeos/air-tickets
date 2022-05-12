from sqlalchemy import Column, String, Enum, Date, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base
from ..enums.documents_enum import DocumentsEnum
from ..enums.gender_enum import GenderEnum


class UserDB(Base):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('document_type', 'document_number'), {'schema': 'ticket'})
    # {'schema': 'ticket'}

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    gender = Column(Enum(GenderEnum))
    document_type = Column(Enum(DocumentsEnum))
    document_number = Column(String)
    date_birth = Column(Date)
    ticket = relationship('TicketDB')


class TicketDB(Base):
    __tablename__ = 'tickets'
    __table_args__ = (UniqueConstraint('user_id', 'flight_time', 'flight_name'), {'schema': 'ticket'})

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    flight_time = Column(String)
    flight_name = Column(String)
    pet = Column(Integer, nullable=True)
    luggage = Column(Integer, nullable=True)
    price = Column(Float)
    user_id = Column(UUID(as_uuid=True), ForeignKey('ticket.users.id'))
    user = relationship('UserDB')
