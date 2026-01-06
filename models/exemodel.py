from database.db import Base
from sqlalchemy import Column , String ,Integer,JSON,ForeignKey
from sqlalchemy.orm import relationship


class Exercise(Base):
    __tablename__ = "exercise"
    exercise_id = Column(Integer,primary_key=True)
    level = Column (String)
    title= Column(String)
    exercise_image = Column(String)
    exercise_video= Column(String)
    instruction = Column (String)
    breathing_tip = Column(String)
    focus_area = Column(JSON)
    category_id = Column(Integer, ForeignKey("category.category_id")) 


