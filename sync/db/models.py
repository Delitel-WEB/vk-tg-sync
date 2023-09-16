from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer


BASE = declarative_base()



class Conversations(BASE):
    """
    Связка беседы ВК с группой Телеграма или
    Свзяка личной беседы ВК с группой Телеграма 
    """

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer)
    tg_id = Column(Integer)