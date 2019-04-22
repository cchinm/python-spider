from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, VARCHAR, DECIMAL
from sqlalchemy import Column

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('yours mysqlurls')
session = sessionmaker(bind=engine)
base = declarative_base()


"""
build database sql

CREATE TABLE `t_code` (
  `code` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `p_code` int(11) DEFAULT NULL,
  `type` int(1) DEFAULT '0',
  UNIQUE KEY `key` (`code`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

"""
class TcityCode(base):

    __tablename__='t_code'

    code = Column('code', INTEGER, primary_key=True)
    name = Column('name', VARCHAR)
    pcode = Column('p_code', INTEGER)



"""
build database sql

CREATE TABLE `t_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT '',
  `lat` decimal(16,7) DEFAULT NULL,
  `lng` decimal(16,7) DEFAULT NULL,
  `area_name` varchar(255) DEFAULT NULL,
  `aid` int(11) DEFAULT '0',
  `cid` int(11) DEFAULT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `kw` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`name`,`aid`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""

class TcompInfo(base):

    __tablename__='t_info'

    id = Column('id', INTEGER, primary_key=True)
    name = Column('name', VARCHAR)
    lat = Column('lat', DECIMAL)
    lng = Column('lng', DECIMAL)
    area_name = Column('area_name', VARCHAR)
    aid = Column('aid', INTEGER)
    cid = Column('cid', INTEGER)
    addr = Column('addr', VARCHAR)
    tags = Column('tags', VARCHAR)
    kw = Column('kw', VARCHAR)