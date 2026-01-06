from pydantic import BaseModel 
from typing import List
class ExerciseCreate(BaseModel):
    level:str
    title: str 
    instruction : str
    breathing_tip : str 
    exercise_image:str
    exercise_video:str
    focus_area : List[str]
    category_id : int  
        
class ExerciseUpdate(BaseModel):
    level: str
    title: str 
    instruction : str
    breathing_tip : str 
    exercise_image:str
    exercise_video:str
    focus_area : List[str]
    category_id : int  

class Focusupdate(BaseModel):
     focus_area:List[str]    