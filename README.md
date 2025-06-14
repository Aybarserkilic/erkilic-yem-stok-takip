# erkilic-yem-stok-takip
# Erkılıç Yem Stok ve Satış Takip Sistemi

## Proje Sahibi
- **İbrahim Aybars Erkılıç**
- **Öğrenci No:** 20010708039
- **Ders:** BTS304 - Veri Tabanı Yönetim Sistemleri

## Proje Hakkında
Bu proje, hayvan yemleri satışı ve stoğu yapan Erkılıç Yem firmasının müşteri, ürün, tedarikçi, sipariş ve ödeme süreçlerinin dijital ortamda yönetilmesi için geliştirilmiştir.  
Proje kapsamında SQL Server üzerinde ilişkisel veritabanı tasarlanmış ve Python Streamlit ile kullanıcı dostu bir arayüz oluşturulmuştur.

## Senaryo Özeti
Firma sahibi, mağazada olup bitenleri ve stok-satış süreçlerini anlık takip edebilmek için tüm işlemlerin merkezi bir sistemde kaydını tutmak istemektedir. Sistem; müşteri-tedarikçi yönetimi, ürün stok takibi, sipariş ve ödeme işlevlerini eksiksiz yerine getirmektedir.

## Temel Özellikler
- Müşteri, tedarikçi, ürün, sipariş ve ödeme kayıtlarının yönetimi
- Tablo arası ilişkiler (1-N, N-N)
- Tüm CRUD işlemleri (ekle, sil, güncelle, listele)
- Saklı yordam, tetikleyici ve fonksiyon kullanımı
- Kısıtlarla veri bütünlüğü
- Otomatik rapor (toplam müşteri, ciro, sipariş, stok vb.)
- Silinen müşteri/ürün loglarının tutulması
- Kullanıcı dostu, güvenli ve modern web arayüzü (Streamlit ile)

## Veritabanı Şeması
![ER Diyagramı](EKLER/er_diyagrami.png)
> **Not:** ER diyagramı ve mantıksal şema dosyası “EKLER” klasöründe yer almaktadır.

## Kurulum ve Kullanım
1. SQL Server (Express veya üstü) ve SSMS kurulu olmalıdır.
2. `erkilic_yem.sql` dosyasını çalıştırarak veritabanını oluşturun.
3. Python 3.10+ yüklü ise:
    ```bash
    pip install streamlit pyodbc pandas
    ```
4. `app.py` dosyasındaki bağlantı ayarlarını (SERVER, DATABASE) kendi bilgisayarınıza göre düzenleyin.
5. Streamlit arayüzünü başlatın:
    ```bash
    streamlit run app.py
    ```

## Kod ve Dosyalar
- `app.py` — Uygulama ana kod dosyası (Streamlit arayüzü)
- `erkilic_yem.sql` — Veritabanı şeması ve örnek veriler
- `EKLER/` — ER diyagramı, mantıksal şema ve ekran görüntüleri
- `README.md` — Bu tanıtım dosyası
- `BTS304_İbrahim_Aybars_Erkilic_Proje_Raporu.docx` — Detaylı rapor

## Ekran Görüntüleri
EKLER klasöründe örnek arayüz ve tablo ekran görüntüleri yer almaktadır.

## Video Sunumu
> [Proje Tanıtım Videosu (YouTube Linki)](https://www.youtube.com/…)  
(Eğer isterseniz buraya kendi YouTube linkinizi ekleyin.)

## Katkı ve Lisans
Proje, BTS304 dersi için hazırlanmıştır ve eğitim amaçlıdır.  
Sorularınız için iletişime geçebilirsiniz.
