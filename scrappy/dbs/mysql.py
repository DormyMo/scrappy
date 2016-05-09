# coding:utf8
__author__ = 'modm'
import MySQLdb
from scrapy.utils import project
from sqlalchemy import Column, String, create_engine, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging


class MysqlClient(object):
    def __init__(self):
        self.settings = project.get_project_settings()  # get settings
        self.MYSQL_HOST = self.settings.get('MYSQL_HOST')
        self.MYSQL_PORT = self.settings.getint('MYSQL_PORT')
        self.MYSQL_USER = self.settings.get('MYSQL_USER')
        self.MYSQL_PASSWD = self.settings.get('MYSQL_PASSWD')
        self.MYSQL_DB = self.settings.get('MYSQL_DB')
        self._conn()

    def _conn(self):
        while True:
            try:
                self.conn = MySQLdb.connect(host=self.MYSQL_HOST, port=self.MYSQL_PORT, user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWD, db=self.MYSQL_DB, charset="utf8")
                break
            except:
                continue

    def _getCursor(self):
        if not self.conn:
            self._conn()
        cur = None
        try:
            cur = self.conn.cursor()
        except:
            self._conn()
        cur = self.conn.cursor()
        return cur


class TestDAO(MysqlClient):
    def __init__(self):
        super(TestDAO, self).__init__()

    def queryOne(self):
        cur = self._getCursor()
        cur.execute("SELECT * FROM test")
        row = cur.fetchone()
        cur.close
        if row:
            return row[0]


class ORM():
    baseCls = None

    def __init__(self):
        settings = project.get_project_settings()
        self.MYSQL_CONN_URI = 'mysql+mysqlconnector://%s:%s@%s:%d/%s' % (
            self.settings.get('MYSQL_USER'), self.settings.get('MYSQL_PASSWD'), self.settings.get('MYSQL_HOST'),
            self.settings.getint('MYSQL_PORT'), self.settings.get('MYSQL_DB'))
        self.engine = self._getEngine()

    @classmethod
    def getBase(cls):
        if not ORM.baseCls:
            ORM.baseCls = declarative_base()
        return ORM.baseCls

    def _getEngine(self):
        engine = create_engine(self.MYSQL_CONN_URI)
        return engine

    def getSession(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        return session

    def initTable(self):
        ORM.baseCls.metadata.create_all(self.engine)

    def add(self, modelObjects):
        try:
            session = self.getSession()
            if type(modelObjects) is list:
                session.add_all(modelObjects)
            else:
                session.merge(modelObjects)
            session.commit()
            session.close()
            return True
        except Exception, e:
            logging.error('mysql orm add error : %s' % (str(e)))
            return False

    def isExist(self, model, modelObjectId):
        session = self.getSession()
        flag = session.query(model.id).filter_by(id=modelObjectId).count() > 0
        session.close()
        return flag
