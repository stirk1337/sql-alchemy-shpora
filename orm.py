from sqlalchemy import create_engine, text, MetaData, Table, Integer, String, BigInteger, ForeignKey, Column, select, \
    insert, Connection, or_, inspect
from sqlalchemy.orm import registry, as_declarative, declared_attr, mapped_column, Mapped, Session, DeclarativeBase
from sqlalchemy.dialects import postgresql, sqlite, oracle

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

session = Session(engine, expire_on_commit=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


Base.metadata.create_all(engine)

user = User(id=1, name='test', age=30)
insp = inspect(user)

print('Is transient?', insp.transient)

session.add(user)
session.flush()
print('Is pending?', insp.pending)

print('Is transient?', insp.transient)

print('Is persistent?', insp.persistent)
session.delete(user)
print('Is deleted?', insp.deleted)
