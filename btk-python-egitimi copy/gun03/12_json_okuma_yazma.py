# -*- coding: utf-8 -*-
"""JSON okuma ve yazma: özet raporu JSON dosyasına kaydedip geri okumak.

NE ÖĞRETİYOR?
    JSON, sözlük ve listelerin metin olarak saklanmış hâlidir. Web servisleri,
    API'ler ve ayar dosyaları JSON kullanır. Python sözlüğü <-> JSON neredeyse aynıdır.
      json.dump(veri, dosya)   : Python -> JSON dosyası
      json.load(dosya)         : JSON dosyası -> Python
      json.dumps / json.loads  : aynısı ama dosya yerine METİN (s = string)
    ensure_ascii=False : Türkçe karakterleri "\\u0130" yerine "İ" olarak yazar
    indent=2           : insanların okuyabileceği girintili biçim

NASIL ÇALIŞTIRILIR?
    python gun03/12_json_okuma_yazma.py

BEKLENEN ÇIKTI (kısaltılmış):
    A birimi: Tuketici
    Yazıldı: outputs/gun03/il_ozeti.json
    JSON geri okundu: 8 il
    Ankara: 107 şikâyet
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cikti = ROOT / "outputs" / "gun03"
cikti.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1) Hazır bir JSON dosyasını okumak (sabahki küçük örnekle aynı dosya)
# ---------------------------------------------------------------------------
with open(ROOT / "data" / "birimler.json", encoding="utf-8") as f:
    birimler = json.load(f)                 # -> Python sözlüğü
print("A birimi:", birimler["A"])
print("Tüm birimler:", birimler)

# ---------------------------------------------------------------------------
# 2) Şikâyetlerden il bazında özet çıkar (iç içe sözlük)
# ---------------------------------------------------------------------------
with (ROOT / "data" / "sikayetler.csv").open(encoding="utf-8", newline="") as dosya:
    kayitlar = list(csv.DictReader(dosya))

ozet = {}
for kayit in kayitlar:
    il = kayit["il"]
    if il not in ozet:                       # ili ilk kez görüyorsak boş kayıt aç
        ozet[il] = {"sikayet": 0, "cozuldu": 0, "islemde": 0}
    ozet[il]["sikayet"] += 1
    if kayit["durum"] == "Çözüldü":
        ozet[il]["cozuldu"] += 1
    elif kayit["durum"] == "İşlemde":
        ozet[il]["islemde"] += 1

rapor = {
    "kaynak": "data/sikayetler.csv",
    "toplam_kayit": len(kayitlar),
    "iller": ozet,                           # sözlüğün içinde sözlük
}

# ---------------------------------------------------------------------------
# 3) JSON dosyasına yaz
# ---------------------------------------------------------------------------
json_dosyasi = cikti / "il_ozeti.json"
with open(json_dosyasi, "w", encoding="utf-8") as f:
    json.dump(rapor, f, ensure_ascii=False, indent=2)
print("Yazıldı:", json_dosyasi.relative_to(ROOT).as_posix())

# ensure_ascii farkını görelim (dosyaya değil ekrana, dumps ile):
print("ensure_ascii=True :", json.dumps({"il": "İzmir"}))
print("ensure_ascii=False:", json.dumps({"il": "İzmir"}, ensure_ascii=False))

# ---------------------------------------------------------------------------
# 4) Geri oku ve kontrol et
# ---------------------------------------------------------------------------
with open(json_dosyasi, encoding="utf-8") as f:
    geri = json.load(f)
print("JSON geri okundu:", len(geri["iller"]), "il")
print("Ankara:", geri["iller"]["Ankara"]["sikayet"], "şikâyet")
print("Toplam tutuyor mu?", sum(v["sikayet"] for v in geri["iller"].values()) == geri["toplam_kayit"])

# Not: JSON'da tarih türü yoktur. date nesnesini doğrudan json.dump'a verirseniz
# "TypeError: Object of type date is not JSON serializable" alırsınız.
# Çözüm: önce metne çevirin -> tarih.isoformat()
