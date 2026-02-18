from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models.exercise_progress import ExerciseProgress
from schemas.exercise_progress import (
    ProgressCreate,
    ProgressResponse
)

router = APIRouter(
    prefix="/progress",
    tags=["Exercise Progress"]
)


# =========================================
# 🔥 COMPLETE DAY
# =========================================
@router.post("/complete-day", response_model=ProgressResponse)
def complete_day(progress: ProgressCreate, db: Session = Depends(get_db)):

    existing = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == progress.user_id,
        ExerciseProgress.level == progress.level,
        ExerciseProgress.category_id == progress.category_id   # ✅ FIXED
    ).first()

    if existing:

        existing.completed_days += 1
        existing.current_day += 1

        if existing.current_day > 7:
            existing.current_day = 1
            existing.current_week += 1

        if existing.current_week > 4:
            existing.current_week = 1
            existing.current_month += 1
            existing.is_month_completed = True

        if existing.current_month > 8:
            existing.is_level_completed = True

        db.commit()
        db.refresh(existing)
        return existing

    # If no progress → create new
    new_progress = ExerciseProgress(
        user_id=progress.user_id,
        level=progress.level,
        category_id=progress.category_id,
        completed_days=1,
        current_day=2,
        current_week=1,
        current_month=1
    )

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return new_progress


# =========================================
# 🔥 GET PROGRESS
# =========================================
@router.get("/{user_id}/{level}/{category_id}", response_model=ProgressResponse)
def get_progress(user_id: int, level: str, category_id: int, db: Session = Depends(get_db)):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level,
        ExerciseProgress.category_id == category_id   # ✅ FIXED
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    return progress


# =========================================
# 🔥 UPDATE PROGRESS
# =========================================
@router.put("/update/{user_id}/{level}/{category_id}", response_model=ProgressResponse)
def update_progress(user_id: int, level: str, category_id: int, db: Session = Depends(get_db)):

    progress = db.query(ExerciseProgress).filter(
        ExerciseProgress.user_id == user_id,
        ExerciseProgress.level == level,
        ExerciseProgress.category_id == category_id   # ✅ FIXED
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")

    progress.current_day += 1
    progress.completed_days += 1

    if progress.current_day > 7:
        progress.current_day = 1
        progress.current_week += 1

    if progress.current_week > 4:
        progress.current_week = 1
        progress.current_month += 1
        progress.is_month_completed = True

    if progress.current_month > 8:
        progress.is_level_completed = True

    db.commit()
    db.refresh(progress)

    return progress



# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from dependencies import get_db
# from models.exercise_progress import ExerciseProgress
# from schemas.exercise_progress import (
#     ProgressCreate,
#     ProgressUpdate,
#     ProgressResponse
# )

# router = APIRouter(
#     prefix="/progress",
#     tags=["Exercise Progress"]
# )


# # 🔥 CREATE PROGRESS
# @router.post("/create", response_model=ProgressResponse)
# def create_progress(progress: ProgressCreate, db: Session = Depends(get_db)):

#     existing = db.query(ExerciseProgress).filter(
#         ExerciseProgress.user_id == progress.user_id,
#         ExerciseProgress.level == progress.level
#     ).first()

#     if existing:
#         raise HTTPException(status_code=400, detail="Progress already exists")

#     new_progress = ExerciseProgress(**progress.dict())

#     db.add(new_progress)
#     db.commit()
#     db.refresh(new_progress)

#     return new_progress


# # 🔥 GET PROGRESS
# @router.get("/{user_id}/{level}", response_model=ProgressResponse)
# def get_progress(user_id: int, level: str, db: Session = Depends(get_db)):

#     progress = db.query(ExerciseProgress).filter(
#         ExerciseProgress.user_id == user_id,
#         ExerciseProgress.level == level
#     ).first()

#     if not progress:
#         raise HTTPException(status_code=404, detail="Progress not found")

#     return progress


# # 🔥 UPDATE PROGRESS (Partial Update)
# @router.put("/update/{user_id}/{level}", response_model=ProgressResponse)
# def update_progress(
#     user_id: int,
#     level: str,
#     progress_update: ProgressUpdate,
#     db: Session = Depends(get_db)
# ):

#     progress = db.query(ExerciseProgress).filter(
#         ExerciseProgress.user_id == user_id,
#         ExerciseProgress.level == level
#     ).first()

#     if not progress:
#         raise HTTPException(status_code=404, detail="Progress not found")

#     update_data = progress_update.dict(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(progress, key, value)

#     db.commit()
#     db.refresh(progress)

#     return progress
