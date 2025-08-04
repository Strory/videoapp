from sqlalchemy.orm import Session
from database_app import models
from database_app.database import SessionLocal


def user_exists(tg_id: int, db: Session) -> models.User | None:
    return db.query(models.User).filter(models.User.tg_id == tg_id).first()


def create_user(tg_id: int, db: Session) -> int:
    user = models.User(tg_id=tg_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def add_video_data(data: dict, tg_id: int):
    db = SessionLocal()
    user = user_exists(tg_id, db)
    if not user:
        user = create_user(tg_id, db)
    user_id = user.id
    try:
        video_data = models.Video(
            user_id=user_id,
            video_path=data['video_path'],
            pose_path=data['pose_path'],
            angle_path=data['angle_path'],
            description=data['description']
        )
        db.add(video_data)
        db.commit()
        db.refresh(video_data)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
