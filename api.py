from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db

# Flask Uygulamasını Başlatıyoruz
app = Flask(__name__)

# Mobil uygulama gibi farklı platformlardan (farklı domain/port) gelecek isteklere 
# izin vermek için CORS (Cross-Origin Resource Sharing) ekliyoruz.
CORS(app)

# Uygulama başlarken veritabanı tablolarının tam olduğundan emin olalım
db.init_db()

# ==============================================================================
# ŞOFÖR İŞLEMLERİ
# ==============================================================================

@app.route('/api/sofor/login', methods=['POST'])
def sofor_login():
    """
    Şoförlerin mobil uygulamadan giriş yapması için kullanılır.
    Beklenen JSON: { "kullanici_adi": "ahmet", "sifre": "sifre123" }
    """
    data = request.json
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')
    
    if not kullanici_adi or not sifre:
        return jsonify({"success": False, "message": "Kullanıcı adı ve şifre gereklidir."}), 400
        
    sofor = db.sofor_dogrula(kullanici_adi, sifre)
    if sofor:
        # Veritabanından gelen veriyi sözlüğe (dict) çeviriyoruz
        return jsonify({"success": True, "data": dict(sofor)}), 200
    else:
        return jsonify({"success": False, "message": "Geçersiz kullanıcı adı veya şifre."}), 401

@app.route('/api/sofor/konum_guncelle', methods=['POST'])
def konum_guncelle():
    """
    Şoförün anlık konumunu merkeze gönderir. Mobil GPS'ten sürekli çağrılabilir.
    Beklenen JSON: { "sofor_id": 1, "enlem": 39.9208, "boylam": 32.8541 }
    """
    data = request.json
    sofor_id = data.get('sofor_id')
    enlem = data.get('enlem')
    boylam = data.get('boylam')
    
    if not sofor_id or enlem is None or boylam is None:
        return jsonify({"success": False, "message": "sofor_id, enlem ve boylam gereklidir."}), 400
        
    db.konum_guncelle(sofor_id, enlem, boylam)
    return jsonify({"success": True, "message": "Konum başarıyla güncellendi."}), 200

@app.route('/api/sofor/alarm_olustur', methods=['POST'])
def alarm_olustur():
    """
    Şoför panik butonuna bastığında çağrılır.
    Beklenen JSON: { "sofor_id": 1, "durum_bilgi": "Kaza oldu", "alarm_tipi": "MANUEL_BUTON" }
    """
    data = request.json
    sofor_id = data.get('sofor_id')
    durum_bilgi = data.get('durum_bilgi', 'ACİL DURUM')
    alarm_tipi = data.get('alarm_tipi', 'MOBIL_PANIK_BUTONU')
    
    if not sofor_id:
        return jsonify({"success": False, "message": "sofor_id gereklidir."}), 400
        
    zaman = db.alarm_olustur(sofor_id, durum_bilgi, alarm_tipi)
    return jsonify({"success": True, "message": "Alarm merkeze iletildi.", "zaman": zaman}), 201

@app.route('/api/sofor/ses_log_ekle', methods=['POST'])
def ses_log_ekle():
    """
    Şoförün sağlıklı/uyumlu yanıtlarını (örn: "iyiyim") kaydeder.
    Beklenen JSON: { "sofor_id": 1, "metin": "Her şey yolunda" }
    """
    data = request.json
    sofor_id = data.get('sofor_id')
    metin = data.get('metin')
    
    if not sofor_id or not metin:
        return jsonify({"success": False, "message": "sofor_id ve metin gereklidir."}), 400
        
    db.ses_logu_ekle(sofor_id, metin)
    return jsonify({"success": True, "message": "Ses logu eklendi."}), 201

@app.route('/api/sofor/vardiya_analizi_kaydet', methods=['POST'])
def vardiya_analiz_kaydet():
    """
    Vardiya analiz sonucunu kaydeder.
    Beklenen JSON: { "sofor_id": 1, "baslangic_metni": "...", "bitis_metni": "...", "analiz_sonucu": "İYİ", "analiz_detay": "..." }
    """
    data = request.json
    sofor_id = data.get('sofor_id')
    baslangic_metni = data.get('baslangic_metni', '')
    bitis_metni = data.get('bitis_metni', '')
    analiz_sonucu = data.get('analiz_sonucu')
    analiz_detay = data.get('analiz_detay', '')
    
    if not sofor_id or not analiz_sonucu:
        return jsonify({"success": False, "message": "sofor_id ve analiz_sonucu gereklidir."}), 400
        
    db.vardiya_ses_kaydet(sofor_id, baslangic_metni, bitis_metni, analiz_sonucu, analiz_detay)
    return jsonify({"success": True, "message": "Vardiya analizi kaydedildi."}), 201


# ==============================================================================
# YOLCU İŞLEMLERİ
# ==============================================================================

@app.route('/api/yolcu/login', methods=['POST'])
def yolcu_login():
    """
    Yolcunun plaka ile otobüse bağlanması için kullanılır.
    Beklenen JSON: { "plaka": "34 ABC 001" }
    """
    data = request.json
    plaka = data.get('plaka')
    
    if not plaka:
        return jsonify({"success": False, "message": "Plaka gereklidir."}), 400
        
    # Boşluklu/büyük harfli plaka aramasını kolaylaştırmak için strip
    sofor = db.sofor_plaka_ile_bul(plaka.strip())
    if sofor:
        return jsonify({"success": True, "data": dict(sofor)}), 200
    else:
        return jsonify({"success": False, "message": "Bu plakaya ait kayıtlı şoför/araç bulunamadı."}), 404

@app.route('/api/yolcu/yorum_ekle', methods=['POST'])
def yolcu_yorum_ekle():
    """
    Yolcunun şoföre/otobüse puan vermesi ve yorum yapması için.
    Beklenen JSON: { "sofor_id": 1, "puan": 5, "etiketler": "Temiz, Güler yüzlü", "serbest_yorum": "Çok iyiydi" }
    """
    data = request.json
    sofor_id = data.get('sofor_id')
    puan = data.get('puan')
    etiketler = data.get('etiketler', '')
    serbest_yorum = data.get('serbest_yorum', '')
    
    if not sofor_id or not puan:
        return jsonify({"success": False, "message": "sofor_id ve puan gereklidir."}), 400
        
    db.yolcu_yorumu_ekle(sofor_id, puan, etiketler, serbest_yorum)
    return jsonify({"success": True, "message": "Yorumunuz başarıyla kaydedildi. Teşekkür ederiz."}), 201


# ==============================================================================
# ADMİN İŞLEMLERİ (MERKEZ)
# ==============================================================================

@app.route('/api/admin/alarmlar', methods=['GET'])
def admin_alarmlar():
    """Tüm acil durum alarmlarını getirir."""
    alarmlar = db.tum_alarmlari_getir()
    return jsonify({"success": True, "data": alarmlar}), 200

@app.route('/api/admin/ses_loglari', methods=['GET'])
def admin_ses_loglari():
    """Tüm ses kayıt geçmişini getirir."""
    loglar = db.tum_ses_loglarini_getir()
    return jsonify({"success": True, "data": loglar}), 200

@app.route('/api/admin/vardiya_kayitlari', methods=['GET'])
def admin_vardiya_kayitlari():
    """Tüm vardiya (yorgunluk) analizlerini getirir."""
    kayitlar = db.vardiya_kayitlarini_getir()
    return jsonify({"success": True, "data": kayitlar}), 200

@app.route('/api/admin/yolcu_yorumlari', methods=['GET'])
def admin_yolcu_yorumlari():
    """Tüm yolcu geri bildirimlerini getirir."""
    yorumlar = db.yolcu_yorumlarini_getir()
    return jsonify({"success": True, "data": yorumlar}), 200

@app.route('/api/admin/konumlar', methods=['GET'])
def admin_konumlar():
    """Tüm araçların son canlı konumlarını getirir."""
    konumlar = db.tum_konumlari_getir()
    return jsonify({"success": True, "data": konumlar}), 200

@app.route('/api/admin/soforler', methods=['GET'])
def admin_soforler():
    """Tüm kayıtlı şoförleri getirir."""
    soforler = db.tum_soforleri_getir()
    return jsonify({"success": True, "data": soforler}), 200


if __name__ == '__main__':
    print("🚀 Mobil API Sunucusu Başlatılıyor...")
    print("🌐 Yerel Ağ Adresi: http://172.20.10.2:5000")
    print("📱 iPhone'dan erişmek için bu adresi kullanabilirsiniz.")
    # host='0.0.0.0' sayesinde yerel ağdaki (aynı wifideki) cihazlar bağlanabilir.
    app.run(host='0.0.0.0', port=5000, debug=True)
