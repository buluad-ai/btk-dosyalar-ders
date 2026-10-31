# -*- coding: utf-8 -*-
"""İsteğe bağlı Streamlit paneli. Sentetik eğitim örneği; doğrudan çalıştırılabilir."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

# Bu dosya yalnızca isteğe bağlı canlı gösterimdir; temel ders için gerekmez.
# Başlat: python -m streamlit run gun07/04_streamlit_opsiyonel.py
# Durdur: terminalde Ctrl+C. Test için --check kullanılır; sunucu açmaz.
import sys
try:
    import streamlit as st
    import pandas as pd
except ImportError:
    print("ATLANDI: streamlit/pandas yok. 02_html_rapor.py kullanın.")
else:
    if "--check" in sys.argv:
        veri = pd.read_csv(ROOT / "data" / "basvurular.csv")
        print("Panel verisi:", len(veri))
    else:
        st.title("Başvuru analiz paneli")
        st.caption("Sentetik eğitim verisi")
        veri = pd.read_csv(ROOT / "data" / "basvurular.csv")
        birim = st.selectbox("Birim", sorted(veri["birim_kodu"].unique()))
        secilen = veri.loc[veri["birim_kodu"] == birim]
        st.metric("Başvuru sayısı", len(secilen))
        st.dataframe(secilen)
        st.bar_chart(secilen.groupby("kategori").size())
