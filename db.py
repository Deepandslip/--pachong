from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base

BASE=declarative_base()
engine=create_engine(
    'mysql+pymysql://root:0000@127.0.0.1:3306/test?charset=utf8',
    max_overflow=500,
    pool_size=100,
    echo=False,
)
class House(BASE):
    __tablename__='house'
    id=Column(Integer,primary_key=True,autoincrement=True)
    block=Column(String(125))
    title=Column(String(125))
    rent=Column(String(125))
    data=Column(Text())

BASE.metadata.create_all(engine)
Session=sessionmaker(engine)
sess=scoped_session(Session)
