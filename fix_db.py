# -*- coding: utf-8 -*-
"""
MongoDB Veritabanı Temizleme ve Sıfırlama Scripti
Kargo ve rotaları temizler; istasyon ve araçları korur.
"""
import database

def fix_database():
    print("=" * 55)
    print("   LOGIROUTE - MONGODB TEMİZLEME VE SIFIRLAMA")
    print("=" * 55)

    if not database.check_connection():
        print("[X] MongoDB sunucusuna bağlanılamadı!")
        return

    db = database.get_db()

    # Rotaları ve kargoları sil
    r_del = db.routes.delete_many({})
    print(f"[OK] {r_del.deleted_count} adet rota silindi.")

    c_del = db.cargos.delete_many({})
    print(f"[OK] {c_del.deleted_count} adet kargo silindi.")

    # Ana Depo Hub kontrolü
    depot = db.stations.find_one({'is_depot': True})
    if not depot:
        sid = database.get_next_id('stations')
        db.stations.insert_one({
            'id': sid,
            'name': 'Marmara Lojistik Ana Hub (Kocaeli)',
            'city': 'Kocaeli',
            'district': 'İzmit',
            'latitude': 40.8225,
            'longitude': 29.9213,
            'is_active': 1,
            'is_depot': True
        })
        print(f"[OK] Ana Lojistik Depo Hub yeniden eklendi (ID: {sid})")
    else:
        print(f"[OK] Ana Lojistik Depo Hub ({depot['name']}) doğrulandı.")

    print("\n[OK] Veritabanı başarıyla sıfırlandı ve temizlendi!")
    print("=" * 55)

if __name__ == '__main__':
    confirm = input("Tüm kargolar ve rotalar silinecek. Emin misiniz? (e/h): ")
    if confirm.lower() == 'e':
        fix_database()
    else:
        print("İptal edildi.")
