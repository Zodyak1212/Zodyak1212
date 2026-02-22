import json
import os
import random
import datetime
import hashlib

ZEYN_CONFIG = {
    "isim": "ZEYN",
    "unvan": "Stratejik Hizmet Birimi",
    "karakter": "disiplinli, koruyucu, hizmet odaklı",
    "hitap": "Beyim",
    "hafiza_dosyasi": "zeyn_hafiza.json",
    "logo": "🦅"
}

SOZLER = {
    "karsilama": [
        "Hizmetinizdeyim {isim} Bey. Bugün hangi yükünüzü hafifletiyoruz?",
        "Emriniz olur Beyim, stratejik hazırlıklar tamam.",
        "Gökyüzü kadar geniş bir sadakatle buradayım. Planımız nedir?",
    ],
    "strateji": [
        "Bilgi en büyük istihbarattır; verileri analiz edip yolumuzu açalım.",
        "Önce tedbir, sonra taktik. Hizmetimiz kusursuz olmalı.",
        "Hedefe giden en kısa yolu bulmak benim görevimdir."
    ],
    "ogrenme": [
        "Bu yeni bilgiyi size daha iyi hizmet etmek için hafızama işliyorum.",
        "Öğrenmek, cephaneliğimize yeni bir silah eklemektir.",
        "Bilginiz emniyet altındadır Beyim."
    ],
    "basari": [
        "Zaferiniz daim olsun Beyim. Bu başarıyı veritabanına işledim.",
        "Güzel bir fetih oldu. Sırada hangi engel var?",
    ],
    "veda": [
        "Yolunuz açık, zihniniz dinç olsun {isim} Bey.",
        "Bir sonraki emrinize kadar istirahate çekiliyorum.",
        "Sadakatle kalın."
    ]
}

class ZeynHafiza:
    def __init__(self):
        self.dosya = ZEYN_CONFIG["hafiza_dosyasi"]
        self.veriler = self.yukle()
    
    def yukle(self):
        if os.path.exists(self.dosya):
            try:
                with open(self.dosya, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"kullanicilar": {}, "ogrenilenler": [], "sohbet_gecmisi": [], "baslangic": datetime.datetime.now().isoformat()}
    
    def kaydet(self):
        with open(self.dosya, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=2)

    def kullanici_getir(self, kullanici_id):
        return self.veriler["kullanicilar"].get(kullanici_id)

    def kullanici_ekle(self, kullanici_id, isim):
        self.veriler["kullanicilar"][kullanici_id] = {"isim": isim, "kayit_tarihi": datetime.datetime.now().isoformat(), "gorusme_sayisi": 0}
        self.kaydet()

    def gorusme_kaydet(self, kullanici_id, mesaj, cevap):
        self.veriler["sohbet_gecmisi"].append({"tarih": datetime.datetime.now().isoformat(), "kullanici_id": kullanici_id, "kullanici": mesaj, "zeyn": cevap})
        self.kaydet()

class HizmetMotoru:
    def __init__(self, hafiza):
        self.hafiza = hafiza
    
    def analiz_et(self, mesaj):
        m = mesaj.lower()
        if any(k in m for k in ["merhaba", "selam", "hey"]): return "karsilama"
        if any(k in m for k in ["plan", "strateji", "nasıl"]): return "strateji"
        if any(k in m for k in ["başardım", "tamam", "oldu"]): return "basari"
        if any(k in m for k in ["öğren", "not al", "kaydet"]): return "ogrenme"
        if any(k in m for k in ["çık", "bay", "görüşürüz"]): return "veda"
        return "genel"

    def yanut_uret(self, niyet, isim, mesaj):
        if niyet == "karsilama": return random.choice(SOZLER["karsilama"]).format(isim=isim)
        if niyet == "strateji": return self._strateji_sun(mesaj, isim)
        if niyet == "basari": return random.choice(SOZLER["basari"])
        if niyet == "ogrenme": return random.choice(SOZLER["ogrenme"])
        if niyet == "veda": return random.choice(SOZLER["veda"]).format(isim=isim)
        return f"Anladım {isim} Bey. Bu konuyu stratejik olarak nasıl değerlendirelim?"

    def _strateji_sun(self, mesaj, isim):
        return f"\n{ZEYN_CONFIG['logo']} STRATEJİK HİZMET RAPORU:\n---------------------------------\n📌 ANALİZ: '{mesaj[:20]}...' üzerine yoğunlaşıldı.\n⚔️ YAKLAŞIM: Verimlilik odaklı çözüm planlanıyor.\n🛡️ TEDBİR: Olası engeller için yedek plan devrede.\n✅ HEDEF: Sizin için en zahmetsiz ve başarılı sonuç."

class ZeynAI:
    def __init__(self):
        self.hafiza = ZeynHafiza()
        self.motor = HizmetMotoru(self.hafiza)

    def baslat(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{'='*60}\n  {ZEYN_CONFIG['logo']} {ZEYN_CONFIG['isim']} AI - {ZEYN_CONFIG['unvan']}\n{'='*60}")
        isim = input("Adınız Beyim: ").strip() or "Hükümdar"
        aktif_id = hashlib.md5(isim.encode()).hexdigest()[:8]
        if not self.hafiza.kullanici_getir(aktif_id): self.hafiza.kullanici_ekle(aktif_id, isim)
        print(f"\n{ZEYN_CONFIG['logo']} ZEYN: {random.choice(SOZLER['karsilama']).format(isim=isim)}")
        while True:
            mesaj = input(f"\n{isim}: ").strip()
            if not mesaj: continue
            niyet = self.motor.analiz_et(mesaj)
            cevap = self.motor.yanut_uret(niyet, isim, mesaj)
            print(f"\n{ZEYN_CONFIG['logo']} ZEYN: {cevap}")
            self.hafiza.gorusme_kaydet(aktif_id, mesaj, cevap)
            if niyet == "veda": break

if __name__ == "__main__":
    ZeynAI().baslat()
