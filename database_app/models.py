from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)

    # Связь с видео (один пользователь - много видео)
    videos = relationship("Video", back_populates="user")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign Key!
    video_path = Column(String)
    pose_path = Column(String)
    angle_path = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())

    # Связь с пользователем (много видео - один пользователь)
    user = relationship("User", back_populates="videos")
