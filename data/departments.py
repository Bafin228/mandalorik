import sqlalchemy as sa
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase

class Department(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    chief = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    members = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=True)
    chief_user = orm.relationship('User')

