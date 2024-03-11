from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from connectDB import Base, engine
from typing import Optional, Annotated, List

from sqlalchemy.orm import relationship

intPK = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]


class Documents(Base):
    __tablename__ = 'documents'

    id: Mapped[intPK]
    path: Mapped[str]
    date: Mapped[date]


class Documents_text(Base):
    __tablename__ = 'documents_text'

    id: Mapped[intPK]
    id_doc: Mapped[int] = mapped_column(ForeignKey('documents.id'))
    text: Mapped[str]


def create_table():
    Base.metadata.create_all(engine)



