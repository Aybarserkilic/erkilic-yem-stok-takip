import streamlit as st
import pandas as pd
import pyodbc
import datetime

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=erkilic_yem;"
    "Trusted_Connection=yes;"
)

st.title("Erkılıç Yem Yönetim Paneli")
tables = [
    "Musteri", "Tedarikci", "Urun", "Siparis", "Siparis_Urun", "Odeme",
    "MusteriLog", "UrunSilLog"
]
table = st.selectbox("Tablo Seçiniz", tables)

def get_id_col(table):
    with pyodbc.connect(conn_str) as conn:
        q = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}' AND COLUMNPROPERTY(object_id(TABLE_NAME), COLUMN_NAME, 'IsIdentity')=1"
        res = pd.read_sql(q, conn)
        if not res.empty:
            return res.iloc[0,0]
        else:
            return None

def get_manual_columns(table):
    with pyodbc.connect(conn_str) as conn:
        query = f"""
            SELECT COLUMN_NAME, COLUMNPROPERTY(object_id(TABLE_NAME), COLUMN_NAME, 'IsIdentity') AS is_identity
            FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'
        """
        columns = pd.read_sql(query, conn)
        return [row.COLUMN_NAME for idx, row in columns.iterrows() if not row.is_identity]

def get_table_df(table):
    with pyodbc.connect(conn_str) as conn:
        if table == "Siparis":
            q = """SELECT s.*, m.Adi_Soyadi as Musteri_Adi 
                   FROM Siparis s
                   LEFT JOIN Musteri m ON s.Musteri_ID = m.Musteri_ID"""
            df = pd.read_sql(q, conn)
        else:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
    return df

# LOG tabloları hariç gösterim/güncelleme/ekleme/silme işlemleri
log_tables = ["MusteriLog", "UrunSilLog"]

df = get_table_df(table)
st.subheader(f"{table} Tablosu")
st.dataframe(df)

if table not in log_tables:
    # Güncelleme (edit)
    id_col = get_id_col(table)
    if id_col:
        st.write("**Kayıt Güncelleme**")
        update_id = st.selectbox(f"Güncellenecek {id_col}:", df[id_col].astype(str))
        if update_id:
            row = df[df[id_col].astype(str) == str(update_id)].iloc[0]
            form_cols = [col for col in df.columns if col != id_col]
            updated_data = {}
            with st.form("edit_form"):
                for col in form_cols:
                    updated_data[col] = st.text_input(col, str(row[col]) if row[col] is not None else "")
                submit_update = st.form_submit_button("Güncelle")
                if submit_update:
                    set_expr = ", ".join(f"[{col}] = ?" for col in form_cols)
                    vals = [updated_data[c] for c in form_cols]
                    vals.append(update_id)
                    sql = f"UPDATE {table} SET {set_expr} WHERE [{id_col}] = ?"
                    try:
                        with pyodbc.connect(conn_str) as conn:
                            conn.execute(sql, vals)
                            conn.commit()
                        st.success("Kayıt güncellendi! Sayfayı yenileyin.")
                    except Exception as e:
                        st.error(f"Hata: {e}")

    # Ürün tablosu için silme
    if table == "Urun":
        st.subheader("Ürün Sil")
        urunler = df[["Urun_ID", "Urun_Adi"]]
        urun_sec = st.selectbox("Silinecek ürünü seçin", urunler.apply(lambda x: f"{x['Urun_ID']} - {x['Urun_Adi']}", axis=1))
        if st.button("Ürünü Sil"):
            urun_id = int(urun_sec.split(" - ")[0])
            try:
                with pyodbc.connect(conn_str) as conn:
                    conn.execute("DELETE FROM Urun WHERE Urun_ID = ?", (urun_id,))
                    conn.commit()
                st.success("Ürün silindi! Sayfayı yenileyin.")
            except Exception as e:
                st.error(f"Silme sırasında hata oluştu: {e}")

    # Kayıt ekleme (TÜM tablolarda, otomatik form)
    st.write("---")
    st.write("**Yeni Kayıt Ekle**")
    try:
        form_cols = get_manual_columns(table)
        form_data = {}
        with st.form(f"insert_form_{table}"):
            for col in form_cols:
                # Yabancı anahtarlar için otomatik selectbox
                if col.endswith("_ID") and col != get_id_col(table):
                    ref_table = ""
                    if col == "Musteri_ID":
                        ref_table = "Musteri"
                    elif col == "Tedarikci_ID":
                        ref_table = "Tedarikci"
                    elif col == "Urun_ID":
                        ref_table = "Urun"
                    elif col == "Siparis_ID":
                        ref_table = "Siparis"
                    elif col == "Odeme_ID":
                        ref_table = "Odeme"
                    if ref_table:
                        options_df = get_table_df(ref_table)
                        if not options_df.empty:
                            display_col = None
                            for ad in ["Adi_Soyadi", "Urun_Adi", "Tedarikci_Adi"]:
                                if ad in options_df.columns:
                                    display_col = ad
                                    break
                            if not display_col:
                                for c in options_df.columns:
                                    if c != options_df.columns[0]:
                                        display_col = c
                                        break
                            if display_col:
                                options = dict(zip(options_df[display_col], options_df[options_df.columns[0]]))
                                selection = st.selectbox(col, list(options.keys()), key=f"{col}_{table}")
                                form_data[col] = options[selection]
                            else:
                                form_data[col] = st.text_input(col, key=f"{col}_{table}")
                        else:
                            form_data[col] = st.text_input(col, key=f"{col}_{table}")
                    else:
                        form_data[col] = st.text_input(col, key=f"{col}_{table}")
                # Tarih alanları için date_input
                elif "Tarih" in col:
                    form_data[col] = st.date_input(col, value=datetime.date.today(), key=f"{col}_{table}")
                # Tip/Tür gibi seçim alanları için selectbox
                elif col == "Musteri_Tipi":
                    form_data[col] = st.selectbox(col, ["Toptan", "Perakende"], key=f"{col}_{table}")
                elif col == "Odeme_Tipi":
                    form_data[col] = st.selectbox(col, ["Nakit", "Kredi Kartı", "Çek", "Havale"], key=f"{col}_{table}")
                elif col == "Urun_Turu":
                    # Özel örnek: Tedarikçiye göre ürün türü dinamik
                    tedarikci_id = form_data.get("Tedarikci_ID", None)
                    urunler_df = get_table_df("Urun")
                    if tedarikci_id:
                        urun_turleri = urunler_df[urunler_df["Tedarikci_ID"] == tedarikci_id]["Urun_Turu"].unique().tolist()
                    else:
                        urun_turleri = ["Büyükbaş", "Küçükbaş", "Karma"]
                    form_data[col] = st.selectbox(col, urun_turleri if urun_turleri else ["Büyükbaş", "Küçükbaş", "Karma"], key=f"{col}_{table}")
                elif col == "Birim":
                    form_data[col] = st.selectbox(col, ["kg", "ton", "çuval"], key=f"{col}_{table}")
                else:
                    form_data[col] = st.text_input(col, key=f"{col}_{table}")
            submitted = st.form_submit_button("Ekle")
            if submitted:
                if any(v == "" for v in form_data.values()):
                    st.error("Lütfen tüm alanları doldurun.")
                else:
                    fields = ", ".join(f"[{col}]" for col in form_data)
                    placeholders = ", ".join("?" for _ in form_data)
                    sql = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
                    with pyodbc.connect(conn_str) as conn:
                        conn.execute(sql, tuple(form_data.values()))
                        conn.commit()
                    st.success("Kayıt eklendi! Sayfayı yenileyin.")
    except Exception as e:
        st.error(f"Kayıt eklenemedi: {e}")

# OTOMATİK RAPOR
st.write("---")
st.write("**Otomatik Rapor**")
if table == "Musteri":
    st.info(f"Toplam müşteri sayısı: {len(df)}")
elif table == "Siparis":
    st.info(f"Toplam sipariş sayısı: {len(df)}")
    if "Toplam_Tutar" in df.columns:
        st.info(f"Toplam ciro: {df['Toplam_Tutar'].sum():.2f} ₺")
elif table == "Urun":
    st.info(f"Toplam ürün: {len(df)}")
    if "Stok_Durumu" in df.columns and "Urun_Adi" in df.columns:
        st.write("Grafiksel özet için matplotlib kurulmalı.")
elif table == "Odeme":
    st.info(f"Toplam ödeme: {len(df)}")
    if "Odeme_Miktari" in df.columns:
        st.info(f"Toplam tahsilat: {df['Odeme_Miktari'].sum():.2f} ₺")
elif table == "MusteriLog":
    st.info(f"Toplam müşteri log kaydı: {len(df)}")
elif table == "UrunSilLog":
    st.info(f"Toplam silinen ürün log kaydı: {len(df)}")
