from sqlalchemy import create_engine, text, MetaData, Table, Integer, String, BigInteger, ForeignKey, Column, select, \
    insert, Connection, or_
from sqlalchemy.orm import registry, as_declarative, declared_attr, mapped_column, Mapped, Session
from sqlalchemy.dialects import postgresql, sqlite, oracle

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
metadata = MetaData()

#
# with engine.connect() as connection:
#     result = connection.execute(text("select 'hello, world'"))
#     for entry in result.scalars():
#         print(entry)


# @as_declarative()
# class AbstractModel:
#     id = Column(Integer, autoincrement=True, primary_key=True)
#
#     @classmethod
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
#
#
# class User(AbstractModel):
#     name: Mapped[str] = mapped_column()
#     fullname: Mapped[str] = mapped_column()
#
#
# class Address(AbstractModel):
#     email: Mapped[str] = mapped_column()
#     user_id = Column(ForeignKey('user.id'))
# # print(User.__table__)
#
#
# with Session(engine) as session:
#     with session.begin():
#         AbstractModel.metadata.create_all(engine)
#         user = User(name='Jack', fullname='Jack Cow')
#         session.add(user)
#
#     with session.begin():
#         res = session.execute(select(User).where(User.id == 1))
#         user = res.scalar()
#         print(user.name)

metadata = MetaData()

user_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('first_name', String(30)),
    Column('second_name', String),
)

address_table = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('email_address', String(30)),
    Column('user_id', ForeignKey('users.id'))
)

metadata.create_all(engine)

stmt = insert(user_table).values(first_name='test1', second_name='test2')

print(stmt)
sqlite_stmt = stmt.compile(engine, postgresql.dialect())
print(stmt.compile(engine, oracle.dialect()))

with engine.begin() as conn:  # type: Connection
    result = conn.execute(stmt)
    print(result.inserted_primary_key)

with engine.begin() as conn:
    result = conn.execute(
        select(
            (user_table.c.first_name + ' ' + user_table.c.second_name).label('fullname'))
        .where(
            user_table.c.id.in_([1, 2])
        )
    )

print(result.mappings().all())

for res in result:  # namedtuple, tuple, .mappings()
    print(res.fullname)
