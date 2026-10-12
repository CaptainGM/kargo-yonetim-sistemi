# -*- coding: utf-8 -*-
"""
Kocaeli İstasyon Koordinatlarını Güncelleme Scripti (MongoDB)
"""
import database

def update_coordinates():
    if not database.check_connection():
        print("[X] MongoDB sunucusuna bağlanılamadı!")
        return

    db = database.get_db()

    updates = [
        ("Umuttepe Kampüsü (KOÜ)", 40.8225, 29.9213, True),
        ("Başiskele", 40.714025, 29.928362, False),
        ("Çayırova", 40.8261, 29.3711, False),
        ("Darıca", 40.7692, 29.3753, False),
        ("Derince", 40.7550, 29.8314, False),
        ("Dilovası", 40.7833, 29.5333, False),
        ("Gebze", 40.8027, 29.4307, False),
        ("Gölcük", 40.72, 29.82, False),
        ("Kandıra", 41.0711, 30.1528, False),
        ("Karamürsel", 40.6917, 29.6167, False),
        ("Kartepe", 40.7533, 30.0224, False),
        ("Körfez", 40.762527, 29.777346, False),
        ("İzmit", 40.7654, 29.9408, False),
    ]

    for name, lat, lon, is_depot in updates:
        res = db.stations.update_one(
            {'name': name},
            {'$set': {'latitude': lat, 'longitude': lon, 'is_depot': is_depot}},
            upsert=True
        )
        print(f"[*] {name}: ({lat}, {lon}) - Güncellendi (Matched: {res.matched_count}, Upserted: {res.upserted_id})")

    print("\n[OK] Tüm istasyon koordinatları başarıyla güncellendi!")

if __name__ == '__main__':
    update_coordinates()
