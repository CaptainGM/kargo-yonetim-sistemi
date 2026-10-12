@echo off
chcp 65001 >nul
title LogiRoute - Kargo ve Lojistik Yonetim Sistemi (MongoDB)
color 0B

echo =========================================================
echo       LOGIROUTE - KARGO & LOJISTIK YONETIM SISTEMI
echo       MongoDB Destekli Akilli Rota Optimizasyonu
echo =========================================================
echo.

cd /d "%~dp0"

if not defined MONGO_URI set "MONGO_URI=mongodb://localhost:27017/"
if not defined MONGO_DB_NAME set "MONGO_DB_NAME=kargo_sistemi"

echo [*] MongoDB Baglanti: %MONGO_URI%
echo [*] Veritabani Adi:   %MONGO_DB_NAME%
echo.
echo [!] Ana Sayfa:                   http://localhost:8000
echo [!] Veritabani Goruntuleyici:    http://localhost:8000/db-view
echo.
echo [*] Varsayilan Kullanicilar:
echo     Yonetici: admin / admin123
echo     Kullanici: user  / user123
echo.
echo =========================================================
echo Sunucu baslatiliyor... Kapatmak icin bu pencereyi kapatin.
echo =========================================================
echo.

python app.py

pause
