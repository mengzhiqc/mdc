#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
import web
import datetime

engine = create_engine('mysql://tools:tools@localhost:3306/tools?charset=utf8',encoding="utf-8",echo=True)

def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # If the above alone doesn't work, uncomment 
        # the following line:
        #web.ctx.orm.expunge_all()

Base = declarative_base()

class Devices(Base):
	__tablename__ = 'devices'

	id = Column(Integer, primary_key=True)
	device_name = Column(String(250))
	device_user = Column(String(100))
	device_type = Column(Integer(10))
	device_udid = Column(String(100))
	belong = Column(Integer)
	description = Column(String(250))
	create_time = Column(DateTime,default=datetime.datetime.utcnow)
	updated_time = Column(DateTime)

	def __init__(self,deviceName,deviceUser,deviceType,udid,belong,description,createTime):
		self.device_name = deviceName
		self.device_user = deviceUser
		self.device_type = deviceType
		self.udid = udid
		self.belong = belong
		self.description = description
		self.create_time = createTime
		self.updated_time = createTime

	def __repr__(self):
		return "<Device('%s','%s','%s','%s','%s')>" %(self.device_name,self.device_user,self.udid,self.device_type,self.belong)

devices_table = Devices.__tablename__
metadata = Base.metadata

if __name__ == "__main__":
	metadata.create_all(engine)
