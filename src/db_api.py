import os
import sys
from contextlib import contextmanager
from typing import ContextManager, Optional, Iterable, Any

from sqlalchemy import (
    Column, Integer,
    String, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class BaseDBError(Exception):
    pass


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)

    def _as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            'productName': self.product_name
        }

    def json(self,
             exclude: Iterable[str] = None) -> dict[str, str]:
        exclude = exclude or ()

        return {
            key: str(value)
            for key, value in self._as_dict().items()
            if key not in exclude
        }


engine = create_engine(os.getenv('DB_URI'))
Base.metadata.create_all(engine)


@contextmanager
def session(**kwargs) -> ContextManager[Session]:
    new_session = Session(bind=engine, expire_on_commit=False, **kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception as e:
        new_session.rollback()
        print(repr(e), file=sys.stderr)
        raise BaseDBError(e) from None
    finally:
        new_session.close()


def get_loan(*,
             loan_id: int) -> Optional[Products]:
    with session() as ses:
        return ses.query(Products).get(loan_id)


def add_loan(*,
             product_name: str) -> None:
    with session() as ses:
        loan = Products(
            product_name=product_name
        )
        ses.add(loan)
