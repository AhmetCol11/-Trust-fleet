const translations = {
    tr: {
        // Global
        "brand_name": "TrustFleet",
        "btn_profile": "👤 Profilim",
        "btn_logout": "🚪 Çıkış Yap",
        
        // Login Page
        "login_title": "🛡️ TrustFleet Sürüş Güvenlik Sistemi",
        "login_subtitle": "Yolcu, Şoför ve Merkez Takip Giriş Portalı",
        "tab_passenger": "👤 Yolcu Girişi",
        "tab_driver": "🚌 Şoför Girişi",
        "tab_admin": "🖥️ Merkez Sistem Girişi",
        "passenger_desc": "Güvenli yolculuk sorgusu yapmak, şoför puanlamak veya acil durum ihbarı göndermek için giriş yapın.",
        "driver_desc": "Sürüş güvenliği analizi, canlı rota simülasyonu ve panik butonu entegreli sürüş paneline erişin.",
        "admin_desc": "Tüm filoyu canlı haritadan izlemek, zaman tüneli ses kayıtlarını ve risk alarmlarını takip etmek için giriş yapın.",
        "username_label": "Kullanıcı Adı",
        "username_placeholder": "Kullanıcı adınızı yazın...",
        "password_label": "Giriş Şifresi",
        "password_placeholder": "Şifrenizi yazın...",
        "btn_login_passenger": "👤 Yolcu Olarak Giriş Yap",
        "btn_login_driver": "🚌 Şoför Olarak Giriş Yap",
        "btn_login_admin": "🛡️ Merkez Sistemine Bağlan",
        "demo_title": "Test & Demo Giriş Bilgileri",
        "demo_desc": "Hızlı akademik testler ve inceleme kolaylığı için önceden tanımlanmış hesaplar:",
        "demo_passenger_info": "🔑 <b>Yolcu Girişi:</b> Herhangi bir şoför hesabı bilgisiyle yolcu kısmından da girerek sorgu yapabilirsiniz (Örn: <code>ahmet</code> / <code>sifre123</code>).",
        "demo_driver_info": "🔑 <b>Şoför Hesapları:</b> <code>ahmet</code> / <code>sifre123</code>, <code>mehmet</code> / <code>sifre456</code>, <code>can</code> / <code>can123</code>",
        "demo_admin_info": "🔑 <b>Admin (Merkez) Hesabı:</b> <code>admin</code> / <code>admin123</code>",

        // Driver Dashboard (index.html)
        "driver_title": "🛡️ Sürüş Güvenlik Paneli (Şoför)",
        "welcome_back": "Hoşgeldiniz",
        "vehicle_label": "Araç: ",
        "not_selected": "Henüz Seçilmedi",
        "change_vehicle": "Aracı Değiştir",
        "plate_selection_title": "Aktif Araç / Plaka Seçimi",
        "plate_selection_desc": "Sürüşe ve vardiyaya başlayabilmek için bugün kullanacağınız aracın plakasını seçin veya girin:",
        "plate_select_placeholder": "-- Popüler Plakalardan Seçin --",
        "plate_input_placeholder": "Veya yeni plaka yazın (Örn: 34 CAN 34)",
        "btn_match_vehicle": "Aracı Eşleştir ve Kilidi Aç",
        "shift_status_active": "Vardiya Aktif (Sürüş Güvenliği İzleniyor)",
        "shift_status_inactive": "Vardiya Kapalı (Sürüş Bekleniyor)",
        "shift_status_desc": "Güvenlik kontrol sisteminin ve panik butonunun aktifleşmesi için lütfen sesli doğrulama ile vardiyanızı başlatın.",
        "btn_start_shift": "Vardiyayı Başlat",
        "btn_end_shift": "Vardiyayı Bitir",
        "emergency_title": "Acil Durum",
        "emergency_desc": "Herhangi bir kaza, arıza veya güvenlik ihlali durumunda aşağıdaki butonu kullanın. Merkeze anında konum ve uyarı iletilecektir.",
        "btn_panic": "PANİK BUTONU",
        "live_route_title": "Canlı Rota Takibi",
        "live_route_desc": "Güzergah üzerindeki seyahatinizi Ankara-Kazan Canlı Rota Simülatörü ile gerçek zamanlı olarak simüle edin.",
        "toggle_simulation": "🚌 Rota Simülasyonunu Başlat",
        "btn_go_back": "Geri Git",
        "btn_take_route": "Yol Al",
        "current_stop_label": "Mevcut Durak:",
        "fixed_location_label": "Mevcut Sabit Konumunuz:",
        "voice_assistant_title": "Akıllı Ses Asistanı",
        "voice_assistant_desc": "Sistem arka planda periyodik olarak yorgunluk ve durum analizi yapar.",
        "assistant_status_label": "Asistan Durumu:",
        "assistant_listening": "Dinlemede (Otomatik)",
        "last_sentence_label": "Son Algılanan Cümle:",
        "no_speech_yet": "Henüz konuşma algılanmadı...",
        "btn_test_assistant": "🤖 Asistanı Test Et (Sesi Dinle)",
        "voice_verify_title": "Sesli Asistan Doğrulama",
        "voice_verify_desc": "Şu an asistan sizi dinliyor... Söylediğiniz sözler aşağıda görüntülenecektir. Hatalı kelimeleri elle düzeltebilirsiniz.",
        "heard_text_label": "Duyulan Metin (Düzenlenebilir):",
        "detecting_speech": "Sözleriniz algılanıyor... Lütfen mikrofonunuza konuşun.",
        "btn_say_again": "Yeniden Söyle",
        "btn_confirm_send": "Onayla ve Gönder",

        // Voice Assistant Prompts
        "prompt_welcome_question": "Merhaba şoför bey, nasılsınız? Kendinizi seyahate başlamak için dinç hissediyor musunuz? Lütfen sesli olarak cevap verin.",
        "prompt_end_question": "Vardiyanız sona ermiştir. Kendinizi nasıl hissediyorsunuz? Yolculuk boyunca herhangi bir sorun veya aşırı yorgunluk yaşadınız mı?",
        "prompt_periodic_question_1": "Nasılsınız? Nasıl hissediyorsunuz? Lütfen uykusuzluk ve genel durumunuzu belirtin.",
        "prompt_periodic_question_2": "Anlaşıldı. Peki yolculuk nasıl gidiyor?",
        "prompt_assistant_success_start": "Harika! Vardiyanız başarıyla başlatıldı. Yolculuk boyunca sürüş güvenliği aktif olarak izlenecektir. İyi sürüşler dilerim.",
        "prompt_assistant_ended": "Vardiyanız sonlandırıldı. Günlük yorgunluk analiz raporunuz veri tabanına işlendi. Teşekkürler.",
        "prompt_assistant_risk_detected": "Dikkat! Yorgunluk veya risk tespit edildi. Acil durum alarmı merkeze iletiliyor!",
        "prompt_assistant_retry": "Dinliyorum, lütfen tekrar cevap verin.",

        // Admin Dashboard (admin.html)
        "admin_panel_title": "🖥️ Filo Güvenlik Merkez Takip Ekranı",
        "admin_subtitle": "Canlı Takip, Akıllı Asistan Alarmları ve Sürüş Raporları",
        "tab_live_alerts": "🚨 Canlı Alarmlar & Bildirimler",
        "tab_timeline": " Zürafalar & Ses Logları", // timeline icon + text
        "tab_timeline_real": "⏳ Zaman Tüneli & Ses Kayıtları",
        "tab_passenger_comments": "⭐ Yolcu Yorumları",
        "tab_map_tracking": "🗺️ Canlı GPS Harita Takibi",
        "live_alerts_section": "🚨 Çok Acil Canlı Bildirimler",
        "live_alerts_desc": "Panik butonları veya asistan tarafından saptanan yorgunluk alarmları anlık düşer.",
        "no_alerts_yet": "Henüz acil alarm tetiklenmedi. Sistem kararlı.",
        "registered_drivers": "🚌 Kayıtlı Şoförler & Personel Giriş Bilgileri",
        "registered_drivers_desc": "Akademik testler için şoförlerin güncel sürüş araçları ve açık sistem şifreleri:",
        "driver_card_user": "Kullanıcı:",
        "driver_card_plate": "Plaka:",
        "driver_card_pass": "Şifre:",
        "timeline_section": "⏳ Kronolojik Sürüş Zaman Tüneli",
        "timeline_desc": "Şoförlerin seyahat boyunca yaptığı sesli asistan görüşmeleri, kelime bazlı yorgunluk analiz sonuçları ve GPS konum kayıtları:",
        "no_timeline_yet": "Henüz herhangi bir sürüş log kaydı bulunamadı.",
        "comments_section": "⭐ Yolcu Değerlendirme Raporları",
        "comments_desc": "Seyahat eden yolcuların şoförler ve araçlar hakkında bıraktığı puan, etiket ve detaylı geri bildirim yorumları:",
        "no_comments_yet": "Henüz herhangi bir yolcu değerlendirmesi gönderilmedi.",
        "map_section": "🗺️ Canlı Filo GPS Harita Takibi",
        "map_desc": "Vardiyası aktif olan tüm araçların simüle edilen koordinatları veya manuel girilen canlı konumları harita üzerinde anlık gösterilir:",
        "map_placeholder": "Lütfen bekleyin, Leaflet haritası yükleniyor...",

        // Passenger Pages (yolcu.html / yolcu_plaka_sorgula.html)
        "passenger_panel_title": "⭐ Güvenli Yolculuk & Şoför Değerlendirme Sistemi",
        "passenger_welcome": "Hoşgeldiniz, ",
        "query_title": "🔍 Otobüs / Plaka Sorgulama",
        "query_desc": "Değerlendirmek veya bildirimde bulunmak istediğiniz otobüsün plakasını seçin:",
        "active_plates_label": "Sistemdeki Demo / Aktif Plakalar (Hızlı Seçim):",
        "plate_input_label": "Plakayı Buraya Yazın:",
        "btn_query_plate": "🔍 Otobüsü Sorgula ve Paneli Aç",
        "eval_title": "⭐ Yolcu Sürüş Değerlendirme Formu",
        "eval_subtitle": "Seyahat kalitesini derecelendirin ve merkeze bilgi iletin.",
        "rating_label": "Sürüş ve Güvenlik Puanınız (1-5 Yıldız):",
        "feedback_labels_title": "Hızlı Durum Etiketleri (Birden Fazla Seçilebilir):",
        "tag_safe": "Güvenli Sürüş",
        "tag_polite": "Kibar Personel",
        "tag_speeding": "Aşırı Hız",
        "tag_phone": "Telefonla Konuşma",
        "tag_drowsy": "Uykulu/Yorgun Şoför",
        "tag_dangerous": "Tehlikeli Makas",
        "comment_textarea_label": "Varsa Ek Görüş / Serbest Yorumunuz:",
        "comment_textarea_placeholder": "Yolculuk deneyiminizi buraya yazabilirsiniz...",
        "btn_submit_feedback": "✅ Geri Bildirimi Merkeze İlet",
        "btn_passenger_panic": "🚨 ACİL İHBAR GÖNDER (KAZA/TEHLİKE)"
    },
    en: {
        // Global
        "brand_name": "TrustFleet",
        "btn_profile": "👤 My Profile",
        "btn_logout": "🚪 Log Out",
        
        // Login Page
        "login_title": "🛡️ TrustFleet Driving Safety System",
        "login_subtitle": "Passenger, Driver, and Control Center Login Portal",
        "tab_passenger": "👤 Passenger Login",
        "tab_driver": "🚌 Driver Login",
        "tab_admin": "🖥️ Control Center Login",
        "passenger_desc": "Log in to check ride safety, rate drivers, or submit emergency incident reports instantly.",
        "driver_desc": "Access the driving panel integrated with driving safety analysis, live route simulation, and a panic button.",
        "admin_desc": "Log in to monitor the fleet on a live map, view voice log timelines, and track safety fatigue alarms.",
        "username_label": "Username",
        "username_placeholder": "Enter your username...",
        "password_label": "Password",
        "password_placeholder": "Enter your password...",
        "btn_login_passenger": "👤 Log In as Passenger",
        "btn_login_driver": "🚌 Log In as Driver",
        "btn_login_admin": "🛡️ Connect to Central System",
        "demo_title": "Test & Demo Credentials",
        "demo_desc": "Pre-defined accounts for quick academic testing and easy review:",
        "demo_passenger_info": "🔑 <b>Passenger Login:</b> You can log in as a passenger using any driver account info (e.g. <code>ahmet</code> / <code>sifre123</code>).",
        "demo_driver_info": "🔑 <b>Driver Accounts:</b> <code>ahmet</code> / <code>sifre123</code>, <code>mehmet</code> / <code>sifre456</code>, <code>can</code> / <code>can123</code>",
        "demo_admin_info": "🔑 <b>Admin Account:</b> <code>admin</code> / <code>admin123</code>",

        // Driver Dashboard (index.html)
        "driver_title": "🛡️ Driving Safety Panel (Driver)",
        "welcome_back": "Welcome back",
        "vehicle_label": "Vehicle: ",
        "not_selected": "Not Selected Yet",
        "change_vehicle": "Change Vehicle",
        "plate_selection_title": "Active Vehicle / Plate Selection",
        "plate_selection_desc": "Select or enter the license plate of the vehicle you will use today to start driving and your shift:",
        "plate_select_placeholder": "-- Select from Popular Plates --",
        "plate_input_placeholder": "Or write a new plate (e.g. 34 CAN 34)",
        "btn_match_vehicle": "Match Vehicle & Unlock",
        "shift_status_active": "Shift Active (Driving Safety Under Supervision)",
        "shift_status_inactive": "Shift Ended (Awaiting Driving)",
        "shift_status_desc": "Please start your shift using voice verification to activate the safety monitoring system and panic button.",
        "btn_start_shift": "Start Shift",
        "btn_end_shift": "End Shift",
        "emergency_title": "Emergency Situation",
        "emergency_desc": "In case of any accident, mechanical failure, or security breach, use the button below. Instant location and alerts will be sent to the control center.",
        "btn_panic": "PANIC BUTTON",
        "live_route_title": "Live Route Tracking",
        "live_route_desc": "Simulate your trip along the route in real-time with the Ankara-Kazan Live Route Simulator.",
        "toggle_simulation": "🚌 Start Route Simulation",
        "btn_go_back": "Go Back",
        "btn_take_route": "Take Route",
        "current_stop_label": "Current Stop:",
        "fixed_location_label": "Your Current Fixed Location:",
        "voice_assistant_title": "Smart Voice Assistant",
        "voice_assistant_desc": "The system periodically performs fatigue and status analysis in the background.",
        "assistant_status_label": "Assistant Status:",
        "assistant_listening": "Listening (Automatic)",
        "last_sentence_label": "Last Detected Sentence:",
        "no_speech_yet": "No speech detected yet...",
        "btn_test_assistant": "🤖 Test Assistant (Listen)",
        "voice_verify_title": "Voice Assistant Verification",
        "voice_verify_desc": "The assistant is listening to you... Your words will be displayed below. You can correct mistakes manually.",
        "heard_text_label": "Heard Text (Editable):",
        "detecting_speech": "Your words are being detected... Please speak into your microphone.",
        "btn_say_again": "Say Again",
        "btn_confirm_send": "Confirm and Send",

        // Voice Assistant Prompts
        "prompt_welcome_question": "Hello driver, how are you? Do you feel vigorous and ready to start the trip? Please answer by voice.",
        "prompt_end_question": "Your shift has ended. How do you feel? Have you experienced any problems or extreme fatigue during the trip?",
        "prompt_periodic_question_1": "How are you? How do you feel? Please state your sleepiness and general condition.",
        "prompt_periodic_question_2": "Understood. So, how is the trip going?",
        "prompt_assistant_success_start": "Great! Your shift started successfully. Driving safety is active and under watch. Have a safe drive.",
        "prompt_assistant_ended": "Your shift is completed. Your daily fatigue analysis report has been saved to the database. Thank you.",
        "prompt_assistant_risk_detected": "Attention! Fatigue or risk detected. Emergency alarm is being sent to the control center!",
        "prompt_assistant_retry": "Listening, please answer again.",

        // Admin Dashboard (admin.html)
        "admin_panel_title": "🖥️ Fleet Safety Control Center Tracking",
        "admin_subtitle": "Live Tracking, Smart Assistant Alarms, and Driving Reports",
        "tab_live_alerts": "🚨 Live Alarms & Notifications",
        "tab_timeline_real": "⏳ Timeline & Voice Records",
        "tab_passenger_comments": "⭐ Passenger Reviews",
        "tab_map_tracking": "🗺️ Live GPS Map Tracking",
        "live_alerts_section": "🚨 Emergency Live Notifications",
        "live_alerts_desc": "Panic buttons or fatigue alarms detected by the assistant appear here instantly.",
        "no_alerts_yet": "No emergency alarms triggered yet. System is stable.",
        "registered_drivers": "🚌 Registered Drivers & Staff Logins",
        "registered_drivers_desc": "Current driving plates and plain-text passwords of drivers for academic review:",
        "driver_card_user": "User:",
        "driver_card_plate": "Plate:",
        "driver_card_pass": "Password:",
        "timeline_section": "⏳ Chronological Ride Timeline",
        "timeline_desc": "Voice assistant conversations, word-based fatigue analysis results, and GPS location records of drivers during rides:",
        "no_timeline_yet": "No ride logs found yet.",
        "comments_section": "⭐ Passenger Evaluation Reports",
        "comments_desc": "Ratings, tags, and detailed feedback comments left by passengers about drivers and vehicles:",
        "no_comments_yet": "No passenger reviews submitted yet.",
        "map_section": "🗺️ Live Fleet GPS Map Tracking",
        "map_desc": "Simulated coordinates or manually entered live locations of all active shift vehicles are shown on the map instantly:",
        "map_placeholder": "Please wait, Leaflet map is loading...",

        // Passenger Pages (yolcu.html / yolcu_plaka_sorgula.html)
        "passenger_panel_title": "⭐ Safe Travel & Driver Evaluation System",
        "passenger_welcome": "Welcome, ",
        "query_title": "🔍 Bus / License Plate Search",
        "query_desc": "Select the license plate of the bus you want to evaluate or report:",
        "active_plates_label": "Demo / Active Plates in System (Quick Select):",
        "plate_input_label": "Enter Plate Here:",
        "btn_query_plate": "🔍 Query Bus and Open Panel",
        "eval_title": "⭐ Passenger Ride Evaluation Form",
        "eval_subtitle": "Rate the quality of travel and send information to the center.",
        "rating_label": "Your Ride & Safety Score (1-5 Stars):",
        "feedback_labels_title": "Quick Status Tags (Select Multiple):",
        "tag_safe": "Safe Driving",
        "tag_polite": "Polite Staff",
        "tag_speeding": "Speeding",
        "tag_phone": "Using Phone",
        "tag_drowsy": "Sleepy/Tired Driver",
        "tag_dangerous": "Dangerous Overtaking",
        "comment_textarea_label": "Your Additional Opinions / Comments:",
        "comment_textarea_placeholder": "You can write your travel experience here...",
        "btn_submit_feedback": "✅ Submit Feedback to Center",
        "btn_passenger_panic": "🚨 SEND EMERGENCY ALERT (ACCIDENT/DANGER)"
    }
};

// Global Translation Engine functions
window.currentLanguage = localStorage.getItem('preferred_lang') || 'tr';

window.getTrans = function(key) {
    if (translations[window.currentLanguage] && translations[window.currentLanguage][key]) {
        return translations[window.currentLanguage][key];
    }
    // Fallback to Turkish
    if (translations.tr[key]) {
        return translations.tr[key];
    }
    return key;
};

window.applyTranslations = function() {
    const lang = window.currentLanguage;
    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            // Check if it's an input or placeholder
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[lang][key];
            } else {
                el.innerHTML = translations[lang][key];
            }
        }
    });
    
    // Update navbar current lang label if exists
    const currentLangLabel = document.getElementById('currentLangLabel');
    if (currentLangLabel) {
        currentLangLabel.textContent = lang.toUpperCase();
    }
};

window.changeLanguage = function(lang) {
    window.currentLanguage = lang;
    localStorage.setItem('preferred_lang', lang);
    window.applyTranslations();
    
    // Dispatch custom event so templates can listen to language switch (e.g. Speech recognition)
    const event = new CustomEvent('languageChanged', { detail: { lang: lang } });
    window.dispatchEvent(event);
};

// Auto-run on DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    window.applyTranslations();
});
