@echo off
chcp 65001 >nul
title Kargo Isletme Sistemi - Kocaeli Universitesi
color 0A

echo ============================================
echo    KARGO ISLETME SISTEMI - YAZLAB 3
echo    Kocaeli Universitesi
echo ============================================
echo.

echo [*] MySQL baglantisi kontrol ediliyor...
echo [*] Sunucu baslatiliyor...
echo.
echo [!] Ana Sayfa: http://localhost:8000
echo [!] Veritabani Goruntuleyici: http://localhost:8000/db-view
echo.
echo [!] Kapatmak icin bu pencereyi kapatin
echo.
echo ============================================

cd /d "%~dp0"
if not defined DB_PASSWORD set "DB_PASSWORD="
set "DB_PORT=3306"
set "DB_HOST=127.0.0.1"
echo [*] DB_PASSWORD ortam degiskeni: (start.bat calistirmadan once "set DB_PASSWORD=..." ile ayarlayin)
echo [*] DB_PORT ortam degiskeni ayarlandi: %DB_PORT%
echo [*] DB_HOST ortam degiskeni ayarlandi: %DB_HOST%
start "Kargo Sunucusu" cmd /C "python app.py"

pause

taskkill /FI "WINDOWTITLE eq Kargo Sunucusu" /T /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1
