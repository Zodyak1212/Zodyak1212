import json
import os
import random
import datetime
import hashlib
import unicodedata
from collections import Counter

# ================= CONFIG =================

ZEYN_CONFIG = {
    "isim": "ZEYN",
    "unvan": "Stratejik Zeka Birimi",
    "hitap": "Beyim",
    "hafiza_dosyasi": "zeyn_hafiza.json",
    "logo": "E"
}

# ================= YARDIMCI =================

def normalize(text):
    text = text.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# ================= HAFIZA =================

class ZeynHafiza:
    def __init__(self):
        self.dosya = ZEYN_CONFIG["hafiza_dosyasi"]
        self.veriler = self.yukle()

    def yukle(self):
        if os.path.exists(self.dosya):
            with open(self.dosya, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "kullanicilar": {},
            "sohbet_gecmisi": [],
            "ogrenilenler": [],
            "kelime_frekans": {},
            "baslangic": datetime.datetime.now().isoformat()
        }

    def kaydet(self):
        with open(self.dosya, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=2)

    def kullanici_getir(self, uid):
        return self.veriler["kullanicilar"].get(uid)

    def kullanici_ekle(self, uid, isim):
        self.veriler["kullanicilar"][uid] = {
            "isim": isim,
            "gorusme_sayisi": 0,
            "kayit": datetime.datetime.now().isoformat()
        }
        self.kaydet()

    def gorusme_arttir(self, uid):
        self.veriler["kullanicilar"][uid]["gorusme_sayisi"] += 1
        self.kaydet()

    def sohbet_kaydet(self, uid, mesaj, cevap):
        self.veriler["sohbet_gecmisi"].append({
            "tarih": datetime.datetime.now().isoformat(),
            "uid": uid,
            "mesaj": mesaj,
            "cevap": cevap
        })
        self.kelime_analizi(mesaj)
        self.kaydet()

    def kelime_analizi(self, mesaj):
        kelimeler = normalize(mesaj).split()
        for k in kelimeler:
            self.veriler["kelime_frekans"][k] = \
                self.veriler["kelime_frekans"].get(k, 0) + 1

    def ogren(self, bilgi):
        self.veriler["ogrenilenler"].append({
            "tarih": datetime.datetime.now().isoformat(),
            "bilgi": bilgi
        })
        self.kaydet()

    def son_konusmalar(self, limit=5):
        return self.veriler["sohbet_gecmisi"][-limit:]

# ================= ZEKA MOTORU =================

class ZekaMotoru:
    def __init__(self, hafiza):
        self.hafiza = hafiza

    def niyet_analiz(self, mesaj):
        m = normalize(mesaj)

        if any(k in m for k in ["merhaba", "selam"]):
            return "karsilama"

        if any(k in m for k in ["öğren", "kaydet", "not al"]):
            return "ogren"

        if any(k in m for k in ["istatistik", "analiz", "rapor"]):
            return "analiz"

        if any(k in m for k in ["plan", "strateji", "nasıl"]):
            return "strateji"

        if any(k in m for k in ["çık", "görüşürüz"]):
            return "veda"

        return "genel"

    def cevap_uret(self, niyet, isim, mesaj):

        if niyet == "karsilama":
            return f"Hizmetinizdeyim {isim} Bey."

        if niyet == "ogren":
            self.hafiza.ogren(mesaj)
            return "Bilgi hafızaya işlendi."

        if
