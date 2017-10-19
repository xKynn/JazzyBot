import sqlalchemy
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine(r'sqlite:///demobot.db', echo=False)
Base = declarative_base(bind=engine)
class User(Base):
    __tablename__ = 'users'
    id = Column(u'id',Integer(), primary_key=True)
    dollas = Column(Integer)
    bio = Column(String)
    last_daily = Column(Integer)
    reminder_time = Column(Integer)
    reminder_msg = Column(String)
    p_type = Column(String)
    p_level = Column(String)
    p_xp = Column(Integer)
    p_typechcount = Column(Integer)
    p_typechtime = Column(Integer)
    p_potion = Column(Integer)
    p_fs = Column(Integer)
    p_wins = Column(Integer)
    p_losses = Column(Integer)
    p_moves = Column(String)
    playlist = Column(String)
    last_respex = Column(Integer)
    respex_left = Column(Integer)
    respex = Column(Integer)
    xp = Column(Integer)
    level = Column(Integer)
    unlocked_bg = Column(String)
    applied_bg = Column(String)
class ServerData(Base):
    __tablename__ = 'serverz'
    server_id = Column(u'server_id',Integer(), primary_key=True)
    welcome_channel_id = Column(Integer)
    welcome_msg = Column(String)
    gbye_msg = Column(String)
    admin_role = Column(Integer)
    mod_role = Column(Integer)
    server_prefix = Column(String)
    reactions_toggle = Column(Integer)
    autorole = Column(String)
class BGs(Base):
    __tablename__ = 'BGs'
    name = Column(u'name', String(), primary_key = True)
    cost = Column(Integer)
    level = Column(Integer)
Base.metadata.create_all()
Session = sessionmaker(bind=engine)