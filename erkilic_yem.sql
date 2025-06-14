-- 1. Veritabanı Oluşturma
CREATE DATABASE erkilic_yem;
GO
USE erkilic_yem;
GO

-- 2. Tabloların Oluşturulması

CREATE TABLE Musteri (
    Musteri_ID INT IDENTITY PRIMARY KEY,
    Adi_Soyadi NVARCHAR(100) NOT NULL,
    Musteri_Tipi NVARCHAR(20) NOT NULL CHECK (Musteri_Tipi IN ('Toptan', 'Perakende')),
    Telefon NVARCHAR(20) NOT NULL UNIQUE,
    Adres NVARCHAR(200)
);

CREATE TABLE Tedarikci (
    Tedarikci_ID INT IDENTITY PRIMARY KEY,
    Tedarikci_Adi NVARCHAR(100) NOT NULL,
    Telefon NVARCHAR(20) NOT NULL,
    Adres NVARCHAR(200)
);

CREATE TABLE Urun (
    Urun_ID INT IDENTITY PRIMARY KEY,
    Urun_Adi NVARCHAR(100) NOT NULL,
    Tedarikci_ID INT FOREIGN KEY REFERENCES Tedarikci(Tedarikci_ID),
    Urun_Turu NVARCHAR(50) NOT NULL,
    Stok_Durumu INT NOT NULL CHECK (Stok_Durumu >= 0),
    Fiyat DECIMAL(10,2) NOT NULL CHECK (Fiyat > 0),
    Birim NVARCHAR(10) NOT NULL
);

CREATE TABLE Siparis (
    Siparis_ID INT IDENTITY PRIMARY KEY,
    Musteri_ID INT FOREIGN KEY REFERENCES Musteri(Musteri_ID),
    Siparis_Tarihi DATE NOT NULL,
    Toplam_Tutar DECIMAL(10,2) NOT NULL CHECK (Toplam_Tutar > 0),
    Siparis_Durumu NVARCHAR(30) NOT NULL DEFAULT 'Hazırlandı'
);

CREATE TABLE Siparis_Urun (
    SiparisUrun_ID INT IDENTITY PRIMARY KEY,
    Siparis_ID INT FOREIGN KEY REFERENCES Siparis(Siparis_ID),
    Urun_ID INT FOREIGN KEY REFERENCES Urun(Urun_ID),
    Adet INT NOT NULL CHECK (Adet > 0),
    Birim_Fiyat DECIMAL(10,2) NOT NULL
);

CREATE TABLE Odeme (
    Odeme_ID INT IDENTITY PRIMARY KEY,
    Musteri_ID INT FOREIGN KEY REFERENCES Musteri(Musteri_ID),
    Siparis_ID INT FOREIGN KEY REFERENCES Siparis(Siparis_ID),
    Odeme_Tipi NVARCHAR(20) NOT NULL CHECK (Odeme_Tipi IN ('Nakit','Kredi Kartı','Çek','Havale')),
    Odeme_Tarihi DATE NOT NULL,
    Odeme_Miktari DECIMAL(10,2) NOT NULL CHECK (Odeme_Miktari > 0)
);

-- 3. Log Tabloları

CREATE TABLE MusteriLog (
    Log_ID INT IDENTITY PRIMARY KEY,
    Musteri_ID INT,
    Adi_Soyadi NVARCHAR(100),
    IslemTarihi DATETIME DEFAULT GETDATE(),
    Islem NVARCHAR(50)
);

CREATE TABLE UrunSilLog (
    Log_ID INT IDENTITY PRIMARY KEY,
    Urun_ID INT,
    Urun_Adi NVARCHAR(100),
    IslemTarihi DATETIME DEFAULT GETDATE(),
    Islem NVARCHAR(50)
);

-- 4. Saklı Yordamlar

GO
CREATE PROCEDURE sp_MusteriEkle
    @Adi_Soyadi NVARCHAR(100),
    @Musteri_Tipi NVARCHAR(20),
    @Telefon NVARCHAR(20),
    @Adres NVARCHAR(200)
AS
BEGIN
    INSERT INTO Musteri (Adi_Soyadi, Musteri_Tipi, Telefon, Adres)
    VALUES (@Adi_Soyadi, @Musteri_Tipi, @Telefon, @Adres)
END
GO

-- 5. Fonksiyon (Örnek: Sipariş toplam ürün adedi)
GO
CREATE FUNCTION fn_SiparisUrunAdedi (@SiparisID INT)
RETURNS INT
AS
BEGIN
    DECLARE @Toplam INT
    SELECT @Toplam = SUM(Adet) FROM Siparis_Urun WHERE Siparis_ID = @SiparisID
    RETURN ISNULL(@Toplam,0)
END
GO

-- 6. Trigger Örnekleri

-- Silinen müşteri loglansın
GO
CREATE TRIGGER trg_MusteriSilLog
ON Musteri
AFTER DELETE
AS
BEGIN
    INSERT INTO MusteriLog (Musteri_ID, Adi_Soyadi, Islem)
    SELECT d.Musteri_ID, d.Adi_Soyadi, 'Silindi'
    FROM deleted d
END
GO

-- Silinen ürün loglansın
GO
CREATE TRIGGER trg_UrunSilLog
ON Urun
AFTER DELETE
AS
BEGIN
    INSERT INTO UrunSilLog (Urun_ID, Urun_Adi, Islem)
    SELECT d.Urun_ID, d.Urun_Adi, 'Silindi'
    FROM deleted d
END
GO

-- 7. Örnek Veri Ekleme

INSERT INTO Tedarikci (Tedarikci_Adi, Telefon, Adres) VALUES
('Yem Sanayi', '5554443322', 'İstanbul'),
('Hayvan Yemleri AŞ', '5553332211', 'Ankara');

INSERT INTO Urun (Urun_Adi, Tedarikci_ID, Urun_Turu, Stok_Durumu, Fiyat, Birim) VALUES
('Karma Yem', 1, 'Büyükbaş', 120, 350.00, 'çuval'),
('Süt Yemi', 2, 'Küçükbaş', 80, 390.00, 'çuval'),
('Buğday Kepeği', 1, 'Karma', 90, 280.00, 'çuval');

INSERT INTO Musteri (Adi_Soyadi, Musteri_Tipi, Telefon, Adres) VALUES
('Ali Demir', 'Toptan', '5321112233', 'Konya'),
('Ayşe Aksoy', 'Perakende', '5352223344', 'Afyon'),
('Veli Yılmaz', 'Toptan', '5363334455', 'Eskişehir');