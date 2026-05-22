def yorgunluk_analizi_yap(baslangic_metni: str, bitis_metni: str, baslangic_suresi: float = 1.0, bitis_suresi: float = 1.0):
    yorgunluk_kelimeleri = [
        "yoruldum", "yorgun", "çok yoruldum", "bitik", "halsiz",
        "uyku", "uyuyakaldım", "uyukluyorum", "gözlerim kapanıyor",
        "baş ağrısı", "başım ağrıyor", "baş dönüyor",
        "mola istiyorum", "kötüyüm", "iyi değilim",
        "zor", "dayanamıyorum", "argın"
    ]

    bas_kelime  = len(baslangic_metni.split()) if baslangic_metni else 0
    bit_kelime  = len(bitis_metni.split())     if bitis_metni     else 0

    bas_hiz = bas_kelime / baslangic_suresi if baslangic_suresi > 0 else 0
    bit_hiz = bit_kelime / bitis_suresi if bitis_suresi > 0 else 0

    tehlikeli   = any(k in bitis_metni.lower() for k in yorgunluk_kelimeleri)
    cok_kisa    = bit_kelime < 2
    
    oransal_yorgunluk = (bas_hiz > 0.5) and (bit_hiz < (bas_hiz * 0.75))
    mutlak_yorgunluk = (bit_hiz > 0) and (bit_hiz < 0.9)

    if tehlikeli:
        return "KÖTÜ", f"⚠️ Tehlike ifadesi algılandı: '{bitis_metni[:60]}'"
    elif oransal_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınızda belirgin bir düşüş var ({bas_hiz:.1f} ➜ {bit_hiz:.1f} kelime/sn). Bu yorgunluk belirtisidir."
    elif mutlak_yorgunluk:
        return "KÖTÜ", f"⚠️ Konuşma hızınız çok yavaş ({bit_hiz:.1f} kelime/sn). Dikkat eksikliği ve yorgunluk riski yüksek."
    elif cok_kisa:
        return "KÖTÜ", f"⚠️ Vardiya sonu yanıtı çok kısa ({bit_kelime} kelime) — yorgunluk şüphesi."
    else:
        return "İYİ",  f"✅ Şoför dinç. Ses ritmi ve konuşma hızı normal (Başlangıç: {bas_hiz:.1f}, Bitiş: {bit_hiz:.1f} kelime/sn)."
