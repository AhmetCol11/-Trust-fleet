import hashlib
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(Sofor, int(id))

class Sofor(UserMixin, db.Model):
    __tablename__ = 'soforler'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ad: Mapped[str] = mapped_column(String(100), nullable=False)
    soyad: Mapped[str] = mapped_column(String(100), nullable=False)
    kullanici_adi: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    arac_plaka: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    sifre_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    sifre_plain: Mapped[Optional[str]] = mapped_column(String(255))

    alarmlar: Mapped[List["Alarm"]] = relationship(back_populates="sofor")
    ses_loglari: Mapped[List["SesLog"]] = relationship(back_populates="sofor")
    vardiya_kayitlari: Mapped[List["VardiyaSesKaydi"]] = relationship(back_populates="sofor")
    yorumlar: Mapped[List["YolcuYorum"]] = relationship(back_populates="sofor")
    konum: Mapped[Optional["AracKonum"]] = relationship(back_populates="sofor", uselist=False)

    def check_password(self, password):
        return self.sifre_hash == hashlib.sha256(password.encode()).hexdigest()
        
    def to_dict(self):
        return {
            "id": self.id,
            "ad": self.ad,
            "soyad": self.soyad,
            "kullanici_adi": self.kullanici_adi,
            "arac_plaka": self.arac_plaka,
            "sifre_hash": self.sifre_hash,
            "sifre_plain": self.sifre_plain
        }

class Alarm(db.Model):
    __tablename__ = 'alarmlar'
    alarm_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sofor_id: Mapped[int] = mapped_column(ForeignKey('soforler.id'), nullable=False)
    tarih_saat: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    durum_bilgi: Mapped[Optional[str]] = mapped_column(Text)
    alarm_tipi: Mapped[str] = mapped_column(String(50), nullable=False)

    sofor: Mapped["Sofor"] = relationship(back_populates="alarmlar")
    
    def to_dict(self):
        return {
            "alarm_id": self.alarm_id,
            "sofor_id": self.sofor_id,
            "sofor_adi": f"{self.sofor.ad} {self.sofor.soyad}" if self.sofor else "",
            "arac_plaka": self.sofor.arac_plaka if self.sofor else "",
            "tarih_saat": self.tarih_saat,
            "alarm_tipi": self.alarm_tipi,
            "durum_bilgi": self.durum_bilgi
        }

class SesLog(db.Model):
    __tablename__ = 'ses_loglari'
    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sofor_id: Mapped[int] = mapped_column(ForeignKey('soforler.id'), nullable=False)
    tarih_saat: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    metin: Mapped[str] = mapped_column(Text, nullable=False)

    sofor: Mapped["Sofor"] = relationship(back_populates="ses_loglari")
    
    def to_dict(self):
        return {
            "log_id": self.log_id,
            "sofor_id": self.sofor_id,
            "sofor_adi": f"{self.sofor.ad} {self.sofor.soyad}" if self.sofor else "",
            "tarih_saat": self.tarih_saat,
            "metin": self.metin
        }

class VardiyaSesKaydi(db.Model):
    __tablename__ = 'vardiya_ses_kayitlari'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sofor_id: Mapped[int] = mapped_column(ForeignKey('soforler.id'), nullable=False)
    baslangic_metni: Mapped[Optional[str]] = mapped_column(Text)
    bitis_metni: Mapped[Optional[str]] = mapped_column(Text)
    analiz_sonucu: Mapped[str] = mapped_column(String(50), nullable=False)
    analiz_detay: Mapped[Optional[str]] = mapped_column(Text)
    tarih_saat: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    sofor: Mapped["Sofor"] = relationship(back_populates="vardiya_kayitlari")

    def to_dict(self):
        return {
            "id": self.id,
            "sofor_id": self.sofor_id,
            "sofor_adi": f"{self.sofor.ad} {self.sofor.soyad}" if self.sofor else "",
            "arac_plaka": self.sofor.arac_plaka if self.sofor else "",
            "baslangic_metni": self.baslangic_metni,
            "bitis_metni": self.bitis_metni,
            "analiz_sonucu": self.analiz_sonucu,
            "analiz_detay": self.analiz_detay,
            "tarih_saat": self.tarih_saat
        }

class YolcuYorum(db.Model):
    __tablename__ = 'yolcu_yorumlari'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sofor_id: Mapped[int] = mapped_column(ForeignKey('soforler.id'), nullable=False)
    puan: Mapped[int] = mapped_column(Integer, nullable=False)
    etiketler: Mapped[Optional[str]] = mapped_column(Text)
    serbest_yorum: Mapped[Optional[str]] = mapped_column(Text)
    tarih_saat: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    sofor: Mapped["Sofor"] = relationship(back_populates="yorumlar")

    def to_dict(self):
        return {
            "id": self.id,
            "sofor_id": self.sofor_id,
            "sofor_adi": f"{self.sofor.ad} {self.sofor.soyad}" if self.sofor else "",
            "arac_plaka": self.sofor.arac_plaka if self.sofor else "",
            "puan": self.puan,
            "etiketler": self.etiketler,
            "serbest_yorum": self.serbest_yorum,
            "tarih_saat": self.tarih_saat
        }

class AracKonum(db.Model):
    __tablename__ = 'arac_konumlari'
    sofor_id: Mapped[int] = mapped_column(ForeignKey('soforler.id'), primary_key=True)
    enlem: Mapped[float] = mapped_column(Float, nullable=False)
    boylam: Mapped[float] = mapped_column(Float, nullable=False)
    son_guncelleme: Mapped[str] = mapped_column(String(50), nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    sofor: Mapped["Sofor"] = relationship(back_populates="konum")

    def to_dict(self):
        return {
            "sofor_id": self.sofor_id,
            "sofor_adi": f"{self.sofor.ad} {self.sofor.soyad}" if self.sofor else "",
            "arac_plaka": self.sofor.arac_plaka if self.sofor else "",
            "kadi": self.sofor.kullanici_adi if self.sofor else "",
            "sifre": self.sofor.sifre_plain if self.sofor else "",
            "enlem": self.enlem,
            "boylam": self.boylam,
            "son_guncelleme": self.son_guncelleme
        }
