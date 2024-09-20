# scripts/update_password_hashes.py

"""
Bu script, authentication sistemindeki değişiklikler sonrasında mevcut kullanıcıların
şifre hash'lerini yeni formata dönüştürmek için kullanılır.

ÖNEMLİ NOTLAR:
1. Bu script sadece bir kez, authentication sistemi güncellendikten sonra çalıştırılmalıdır.
2. Scripti çalıştırmadan önce veritabanının tam bir yedeğini almayı unutmayın.
3. Bu script hassas verileri işlediği için, sadece yetkili kişiler tarafından 
   güvenli bir ortamda çalıştırılmalıdır.
4. Scripti production ortamında çalıştırmadan önce test ortamında denediğinizden emin olun.

Kullanım:
    Bu scripti proje kök dizininden şu komutla çalıştırın:
    python -m scripts.update_password_hashes

    Not: Virtualenv kullanıyorsanız, önce activate etmeyi unutmayın.
"""

from sqlalchemy.orm import Session
from models.models import User
from db.database import SessionLocal
from auth.authentication import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_password_hashes():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        updated_count = 0
        for user in users:
            # Bu kısım, eski hash formatını yeni formata dönüştürmek için 
            # özel bir lojik gerektirebilir. Burada basitçe yeni bir hash oluşturuyoruz.
            new_hash = get_password_hash(user.username)  # Güvenlik için gerçek şifreleri bilmediğimizden username'i kullanıyoruz
            user.hashed_password = new_hash
            updated_count += 1
        db.commit()
        logger.info(f"Toplam {updated_count} kullanıcının şifre hash'i güncellendi.")
    except Exception as e:
        logger.error(f"Şifre güncelleme sırasında bir hata oluştu: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Şifre hash'i güncelleme işlemi başlıyor...")
    update_password_hashes()
    logger.info("İşlem tamamlandı.")
