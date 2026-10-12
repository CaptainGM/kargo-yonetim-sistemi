# -*- coding: utf-8 -*-
"""
MongoDB Veritabanı Durum Kontrol Raporu
"""
import database

def check_database():
    print("=" * 55)
    print("   LOGIROUTE - MONGODB VERİTABANI DURUM RAPORU")
    print("=" * 55)

    if not database.check_connection():
        print("[X] MongoDB sunucusuna bağlanılamadı!")
        return

    db = database.get_db()
    print(f"[*] Veritabanı Adı: {db.name} (MongoDB)")

    # 1. İstasyonlar
    station_count = db.stations.count_documents({})
    print(f"\n[İSTASYONLAR] Toplam: {station_count}")
    for st in db.stations.find().sort('id', 1):
        depot_tag = " [DEPO]" if st.get('is_depot') else ""
        print(f"  {st.get('id')}: {st.get('name')}{depot_tag} ({st.get('latitude')}, {st.get('longitude')})")

    # 2. Araçlar
    vehicle_count = db.vehicles.count_documents({})
    print(f"\n[ARAÇLAR] Toplam: {vehicle_count}")
    for v in db.vehicles.find().sort('id', 1):
        owned = "Özmal" if v.get('is_owned') else "Kiralık"
        print(f"  {v.get('id')}: {v.get('name')} ({v.get('capacity')} kg) - {owned}")

    # 3. Bekleyen Kargolar
    pending_count = db.cargos.count_documents({'status': 'pending'})
    print(f"\n[BEKLEYEN KARGOLAR] Toplam: {pending_count}")
    stations_map = {s['id']: s.get('name') for s in db.stations.find()}
    for c in db.cargos.find({'status': 'pending'}).sort('id', 1).limit(10):
        st_name = stations_map.get(c.get('station_id'), 'Bilinmiyor')
        print(f"  ID:{c.get('id')} - {st_name} - {c.get('weight')} kg - Teslimat: {c.get('delivery_date')}")
    if pending_count > 10:
        print(f"  ... ve {pending_count - 10} kargo daha")

    # 4. Atanmış Kargolar ve Toplam
    assigned_count = db.cargos.count_documents({'status': 'assigned'})
    total_cargos = db.cargos.count_documents({})
    all_cargos = list(db.cargos.find())
    total_weight = sum(c.get('weight', 0) for c in all_cargos)
    print(f"\n[ATANMIŞ KARGOLAR] Toplam: {assigned_count}")
    print(f"[TÜM KARGOLAR] {total_cargos} adet, {total_weight:.1f} kg")

    # 5. Rotalar
    route_count = db.routes.count_documents({})
    print(f"\n[ROTALAR] Toplam: {route_count}")
    for r in db.routes.find().sort('created_at', -1).limit(5):
        print(f"  ID:{r.get('id')} - {r.get('vehicle_name')} - {r.get('total_distance')} km - {r.get('total_cost')} TL ({r.get('cargo_count')} kargo)")

    # 6. Kullanıcılar
    user_count = db.users.count_documents({})
    print(f"\n[KULLANICILAR] Toplam: {user_count}")
    for u in db.users.find().sort('id', 1):
        print(f"  ID:{u.get('id')} - {u.get('username')} ({u.get('role')}) - {u.get('email')}")

    print("\n" + "=" * 55)

if __name__ == '__main__':
    check_database()
