import pytest

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta

from simon.models.matcher import Base


database_url = "sqlite:///:memory:"


def create_model(Base: DeclarativeMeta):
    """ Creates a model from a declarative base class.
    """
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    return engine


def test_model_valid():
    try:
        create_model(Base)
    except SQLAlchemyError as e:
        pytest.fail("Unexpected " + e.__class__.__name__)


def test_model_tables_exist():
    tables = Base.metadata.tables
    engine = create_model(Base)

    for name in inspect(engine).get_table_names():
        assert name in tables
