# -*- coding: utf-8 -*-
# type: ignore
"""Veritabanı durum kontrolü"""
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

def check_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(buffered=True)

    try:
        print("=" * 50)
        print("VERİTABANI DURUM RAPORU")
        print("=" * 50)

       
        cursor.execute("SELECT COUNT(*) FROM stations")
        result = cursor.fetchone()
        station_count = result[0] if result else 0
        print(f"\n[İSTASYONLAR] Toplam: {station_count}")
        
        cursor.execute("SELECT id, name FROM stations ORDER BY id")
        for r in cursor.fetchall():
            print(f"  {r[0]}: {r[1]}")

     
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        result = cursor.fetchone()
        vehicle_count = result[0] if result else 0
        print(f"\n[ARAÇLAR] Toplam: {vehicle_count}")
        
        cursor.execute("SELECT id, name, capacity FROM vehicles ORDER BY id")
        for r in cursor.fetchall():
            print(f"  {r[0]}: {r[1]} ({r[2]} kg)")

       
        cursor.execute("SELECT COUNT(*) FROM cargos WHERE status='pending'")
        result = cursor.fetchone()
        pending_count = result[0] if result else 0
        print(f"\n[BEKLEYEN KARGOLAR] Toplam: {pending_count}")
        
        if pending_count and pending_count > 0:
            cursor.execute("""
                SELECT c.id, s.name, c.weight, c.delivery_date 
                FROM cargos c 
                JOIN stations s ON c.station_id = s.id 
                WHERE c.status='pending' 
                ORDER BY c.id
            """)
            for r in cursor.fetchall():
                print(f"  ID:{r[0]} - {r[1]} - {r[2]}kg - Tarih:{r[3]}")

        
        cursor.execute("SELECT COUNT(*) FROM cargos WHERE status='assigned'")
        result = cursor.fetchone()
        assigned_count = result[0] if result else 0
        print(f"\n[ATANMIŞ KARGOLAR] Toplam: {assigned_count}")

       
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(weight), 0) FROM cargos")
        result = cursor.fetchone()
        if result:
            total_count = result[0] if result[0] else 0
            total_weight = float(result[1]) if result[1] else 0.0
            print(f"\n[TÜM KARGOLAR] {total_count} adet, {total_weight:.1f} kg")
        else:
            print("\n[TÜM KARGOLAR] 0 adet, 0.0 kg")

       
        cursor.execute("SELECT COUNT(*) FROM routes")
        result = cursor.fetchone()
        route_count = result[0] if result else 0
        print(f"\n[ROTALAR] Toplam: {route_count}")

        print("\n" + "=" * 50)

    except Error as e:
        print(f"Veritabanı Hatası: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_database()
