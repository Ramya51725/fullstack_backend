from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.exercise_progress import ExerciseProgress
from schemas.exercise_progress import (
    ProgressCreate,
    ProgressUpdate,
    ProgressResponse
)

router = APIRouter(
    prefix="/progress",
    tags=["Exercise Progress"]
)


@router.post("/update/{user_id}/{level}/{category_id}")
def update_progress(user_id: int, level: str, category_id: int, db: Session = Depends(get_db)):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level,
        ExerciseProgress.category_id == category_id
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    progress.completed_exercises = 6  # ✅ default 6
    progress.current_day += 1
    progress.completed_days += 1

    if progress.current_day > 7:
        progress.current_day = 1
        progress.current_week += 1

    if progress.current_week > 4:
        progress.current_week = 1
        progress.current_month += 1

    db.commit()
    db.refresh(progress)

    return progress




# 🔥 GET PROGRESS
@router.get("/{user_id}/{level}", response_model=ProgressResponse)
def get_progress(user_id: int, level: str, db: Session = Depends(get_db)):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    return progress


# 🔥 UPDATE PROGRESS (Partial Update)
@router.put("/update/{user_id}/{level}", response_model=ProgressResponse)
def update_progress(
    user_id: int,
    level: str,
    progress_update: ProgressUpdate,
    db: Session = Depends(get_db)
):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    update_data = progress_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(progress, key, value)

    db.commit()
    db.refresh(progress)

    return progress
