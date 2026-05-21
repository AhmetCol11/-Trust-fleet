from typing import Optional
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    sofor_profili: Mapped[Optional["Sofor"]] = relationship(back_populates="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Sofor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    ad_soyad: Mapped[str] = mapped_column(String(120))
    tc_kimlik: Mapped[str] = mapped_column(String(11), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
    user: Mapped["User"] = relationship(back_populates="sofor_profili")
    alarmlar: Mapped[list["Alarm"]] = relationship(back_populates="sofor")

class Alarm(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    alarm_turu: Mapped[str] = mapped_column(String(50))
    tarih: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    sofor_id: Mapped[int] = mapped_column(ForeignKey('sofor.id'))
    
    sofor: Mapped["Sofor"] = relationship(back_populates="alarmlar")
