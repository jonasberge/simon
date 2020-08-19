import re
import sqlite3

from sqlalchemy import event
from sqlalchemy import (Column, Integer, String,
                        ForeignKey, CheckConstraint, Index)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship


class Base:
    @declared_attr
    def __tablename__(cls):
        """ The `Class` name converted from CamelCase to snake_case. """
        return re.sub(r'(.+)([A-Z])', r'\1_\2', cls.__name__).lower()


class BaseEntity(Base):
    """ Base for an entity that has a single surrogate primary key. """

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
BaseEntity = declarative_base(cls=BaseEntity, metadata=Base.metadata)


class Group(BaseEntity):
    """ Entity for grouping names into separate units.

        This allows filtering out subsets of names that may not be relevant
        for a specific query.
    """

    name = Column(String, unique=True)


class Name(BaseEntity):
    """ Entity for a name.
    """

    name = Column(String, nullable=False)

    group_id = Column(Integer, ForeignKey('group.id'), index=True)
    group = relationship('Group', back_populates='names')

    bigrams = relationship('Name_Bigram', back_populates='name')


class Bigram(BaseEntity):
    """ Entity for a `Name`'s bigram.

        A "`Bigram`" is really either a uni- or bigram because some words
        might only have a single character but are required to be stored in
        the database. This class is still named this way because the concept
        of a bigram reflects its purpose in the best possible way.
    """

    __table_args__ = (  # TODO: try if removing all CheckConstraint-s is faster
        CheckConstraint(" bigram <> '' "),
    )

    bigram = Column(String(length=2), nullable=False, index=True)

    group_id = Column(Integer, ForeignKey('group.id'), index=True)
    group = relationship('Group', back_populates='bigrams')

    names = relationship('Name_Bigram', back_populates='bigram')


class NameBigram(Base):
    """ Many-to-many association between `Name` and `Bigram`.

        Names are split into words and their respective bigrams which is
        reflected by the `word_index` and `word_bigram_index` columns.

        `(name_id, word_index, word_bigram_index)` cannot be used as the
        primary key here because the algorithm may insert multiple `Bigram`s
        for the same position in a name.
    """

    __table_args__ = (
        CheckConstraint(" word_index >= 0 "),
        CheckConstraint(" word_bigram_index >= 0 "),
        Index('ix_name_bigram_name_positions',
              'name_id', 'word_index', 'word_bigram_index')
    )

    name_id = Column(Integer, ForeignKey('name.id'), primary_key=True)
    word_index = Column(Integer, primary_key=True)
    word_bigram_index = Column(Integer, primary_key=True)

    bigram_id = Column(Integer, ForeignKey('bigram.id'),
                       nullable=False, primary_key=True, index=True)

    name = relationship("Name", back_populates="bigrams")
    bigram = relationship("Bigram", back_populates="names")


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(connection, *args):
    """ Enable SQLite foreign key support and set the journal mode to WAL.
    """
    if type(connection) is sqlite3.Connection:
        cursor = connection.cursor()
        cursor.execute(" PRAGMA foreign_keys = ON ")
        # TODO: enable WAL journaling mode where it's actually needed.
        cursor.execute(" PRAGMA journal_mode = WAL ")
        cursor.close()
