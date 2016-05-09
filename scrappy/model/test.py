# coding:utf8
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime
from scrappy.dbs.mysql import ORM
from datetime import datetime

Base = ORM.getBase()


class Test(Base):
    # table name:
    __tablename__ = 'test'

    # table columns:
    id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(String(25))
    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now)
    date_delete = Column(DateTime)

    def beforeAdd(self, kwargs):
        pass

    def whenDunplicate(self):
        pass


if __name__ == '__main__':
    # create all table
    orm = ORM()
    orm.initTable()
