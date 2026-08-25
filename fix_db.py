# -*- coding: utf-8 -*-
# type: ignore
"""Veritabanı düzeltme ve temizleme scripti"""
import os
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'kargo_sistemi'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def fix_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(buffered=True)
    
    try:
        print("=" * 50)
        print("VERİTABANI TEMİZLEME")
        print("=" * 50)
        
     
        cursor.execute("DELETE FROM route_cargos")
        print("[OK] route_cargos temizlendi")
        
        cursor.execute("DELETE FROM routes")
        print("[OK] routes temizlendi")
        
        
        cursor.execute("DELETE FROM cargos")
        print("[OK] cargos temizlendi")
       
        cursor.execute("SELECT id, name FROM stations ORDER BY id")
        stations = cursor.fetchall()
        print(f"\n[İSTASYONLAR] {len(stations)} adet:")
        
        has_umuttepe = False
        for row in stations:
            station_id = row[0]
            station_name = str(row[1]) if row[1] else ""
            is_depot = 'umuttepe' in station_name.lower() or 'koü' in station_name.lower() or 'kampüs' in station_name.lower()
            if is_depot:
                has_umuttepe = True
                print(f"  {station_id}: {station_name} [DEPO]")
            else:
                print(f"  {station_id}: {station_name}")
        
        if not has_umuttepe:
            print("\n[!] Umuttepe Kampüsü bulunamadı, ekleniyor...")
            cursor.execute("INSERT INTO stations (name, latitude, longitude) VALUES ('Umuttepe Kampüsü (KOÜ)', 40.8225, 29.9213)")
            print("[OK] Umuttepe Kampüsü eklendi")
        
        conn.commit()
        
        print("\n" + "=" * 50)
        print("[OK] Veritabanı temizlendi!")
        print("=" * 50)
        
    except Error as e:
        print(f"Veritabanı Hatası: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    confirm = input("Tüm kargolar ve rotalar silinecek. Emin misiniz? (e/h): ")
    if confirm.lower() == 'e':
        fix_database()
    else:
        print("İptal edildi.")
