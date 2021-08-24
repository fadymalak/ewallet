# from amazon.ion.simple_types import IonPyBool , IonPyFloat , IonPyBytes
# from amazon.ion.simpleion import loads , dumps
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Table,Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from .database2 import Base
# Base = database2.Base


class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer,primary_key=True,autoincrement=True)
    mail= Column(String)
    balance = Column(Float)
    
    
    
class Transcation(Base):
    __tablename__ = "transcation"
    id = Column(Integer,primary_key=True,autoincrement=True)
    type = Column(String)
    date= Column(DateTime)
    comment = Column(String)
    amount = Column(Float)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    is_deleted = Column(Integer)
    reference = Column(Integer)

