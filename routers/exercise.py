from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.exemodel import Exercise
from schemas.exeschema import ExerciseCreate, ExerciseUpdate, Focusupdate
from dependencies import get_db

router = APIRouter(
    prefix="/exercise",
    tags=["Exercise"]
)

@router.get("/exercise")
def get_all(db: Session = Depends(get_db)):
    return db.query(Exercise).all()

@router.get("/exercise/{id}")
def get_exercise_by_id(id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).get(id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.get("/by-category-level")
def get_exercise_by_category_and_level(
    category_id: int,
    level: str,
    db: Session = Depends(get_db)
):
    exercises = db.query(Exercise).filter(
        Exercise.category_id == category_id,
        Exercise.level == level
    ).all()

    return exercises


@router.post("/create")
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    new_exercise = Exercise(
        level=exercise.level,
        title=exercise.title,
        instruction=exercise.instruction,
        breathing_tip=exercise.breathing_tip,
        exercise_image=exercise.exercise_image,
        exercise_video=exercise.exercise_video,
        focus_area=exercise.focus_area,
        category_id=exercise.category_id,
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@router.put("/update/{id}")
def update_exercise(id: int, exercise: ExerciseUpdate, db: Session = Depends(get_db)):
    exercise_update = db.query(Exercise).filter(Exercise.exercise_id == id).first()
    if not exercise_update:
        raise HTTPException(status_code=404, detail="Exercise not found")

    exercise_update.level = exercise.level
    exercise_update.title = exercise.title
    exercise_update.instruction = exercise.instruction
    exercise_update.breathing_tip = exercise.breathing_tip
    exercise_update.exercise_image = exercise.exercise_image
    exercise_update.exercise_video = exercise.exercise_video
    exercise_update.focus_area = exercise.focus_area
    exercise_update.category_id = exercise.category_id

    db.commit()
    db.refresh(exercise_update)
    return exercise_update




@router.delete("/delete/{id}")
def delete_exercise(id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.exercise_id == id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(exercise)
    db.commit()
    return {"msg": "Exercise deleted successfully"}



@router.get("/category/{category_id}")
def get_exercise_by_category(category_id: int, db: Session = Depends(get_db)):
    exercises = db.query(Exercise).filter(
        Exercise.category_id == category_id
    ).all()

    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found")

    return exercises


@router.patch("/focus/{exercise_id}")
def update_focus(exercise_id: int, update_focus: Focusupdate, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    exercise.focus_area = update_focus.focus_area
    db.commit()
    db.refresh(exercise)
    return exercise

