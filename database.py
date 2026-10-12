# -*- coding: utf-8 -*-
"""
Kargo & Lojistik Yönetim Sistemi - MongoDB Veritabanı Yöneticisi
"""
import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional
import pymongo
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ConnectionFailure, DuplicateKeyError

from config import MONGO_URI, MONGO_DB_NAME

_client: Optional[MongoClient] = None


def get_mongo_client() -> MongoClient:
    """Tekil MongoClient bağlantısı sağlar."""
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    """MongoDB veritabanı örneği döndürür."""
    client = get_mongo_client()
    return client[MONGO_DB_NAME]


def check_connection() -> bool:
    """MongoDB sunucusuna ping atarak bağlantıyı doğrular."""
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"[!] MongoDB Bağlantı Hatası: {e}")
        return False


def get_next_id(collection_name: str) -> int:
    """
    Belirli bir koleksiyon için otomatik artan tam sayı kimlik (auto-increment id) üretir.
    Frontend ve optimizasyon algoritmalarıyla %100 uyumluluk sağlar.
    """
    db = get_db()
    counter = db.counters.find_one_and_update(
        {'_id': collection_name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return int(counter['seq'])


def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """MongoDB belgesini JSON formatına hazır hale getirir."""
    if not doc:
        return None
    data = dict(doc)
    if '_id' in data:
        data['_mongo_id'] = str(data['_id'])
        del data['_id']
    for k, v in list(data.items()):
        if isinstance(v, datetime):
            data[k] = v.strftime('%Y-%m-%d %H:%M:%S')
    return data


def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """MongoDB belge listesini serialize eder."""
    return [serialize_doc(d) for d in docs if d is not None]


def init_database() -> bool:
    """
    MongoDB koleksiyonlarını ve indekslerini hazırlar;
    varsayılan kullanıcıları, istasyonları, araçları ve parametreleri tohumlar (seed eder).
    """
    if not check_connection():
        print(f"[X] MongoDB sunucusuna bağlanılamadı ({MONGO_URI}). Lütfen MongoDB servisinin çalıştığından emin olun.")
        return False

    db = get_db()
    print(f"[*] MongoDB bağlantısı başarılı: '{MONGO_DB_NAME}' veritabanı denetleniyor...")

    # 1. İndeksler
    try:
        db.users.create_index('username', unique=True)
        db.users.create_index('email', unique=True, sparse=True)
        db.stations.create_index('name', unique=True)
        db.cargos.create_index([('status', pymongo.ASCENDING), ('delivery_date', pymongo.ASCENDING)])
        db.routes.create_index([('created_at', pymongo.DESCENDING)])
        db.password_reset_codes.create_index('user_id')
        db.password_reset_codes.create_index('expires_at')
    except Exception as e:
        print(f"[!] İndeks oluşturma uyarısı: {e}")

    # 2. Varsayılan Kullanıcılar
    default_users = [
        {
            'username': 'admin',
            'email': 'admin@kargo.local',
            'password': hashlib.sha256('admin123'.encode()).hexdigest(),
            'plain_password': 'admin123',
            'role': 'admin'
        },
        {
            'username': 'user',
            'email': 'user@kargo.local',
            'password': hashlib.sha256('user123'.encode()).hexdigest(),
            'plain_password': 'user123',
            'role': 'user'
        }
    ]

    for u in default_users:
        existing = db.users.find_one({'username': u['username']})
        if not existing:
            uid = get_next_id('users')
            db.users.insert_one({
                'id': uid,
                'username': u['username'],
                'email': u['email'],
                'password': u['password'],
                'plain_password': u['plain_password'],
                'role': u['role'],
                'created_at': datetime.now()
            })
            print(f"  [+] Varsayılan kullanıcı eklendi: {u['username']} (ID: {uid})")

    # 3. Türkiye Geneli 81 İl ve İlçe İstasyonları (260+ İstasyon)
    try:
        from data_turkey import TURKEY_STATIONS, EXPANDED_VEHICLES, LOGISTICS_PARAMS
    except ImportError:
        TURKEY_STATIONS = []
        EXPANDED_VEHICLES = []
        LOGISTICS_PARAMS = {}

    if db.stations.count_documents({}) != len(TURKEY_STATIONS):
        db.stations.delete_many({})
        db.counters.update_one({'_id': 'stations'}, {'$set': {'seq': 0}}, upsert=True)
        for st in TURKEY_STATIONS:
            sid = get_next_id('stations')
            db.stations.insert_one({
                'id': sid,
                'name': st['name'],
                'city': st.get('city', ''),
                'district': st.get('district', ''),
                'latitude': float(st['latitude']),
                'longitude': float(st['longitude']),
                'station_type': st.get('station_type', 'branch'),
                'daily_capacity': int(st.get('daily_capacity', 10000)),
                'is_active': 1,
                'is_depot': st.get('is_depot', False)
            })
        print(f"  [+] {len(TURKEY_STATIONS)} adet Türkiye geneli il ve ilçe istasyonu eklendi.")

    # 4. Genişletilmiş ve Çeşitlendirilmiş Araç Filosu
    db.vehicles.delete_many({})
    db.counters.update_one({'_id': 'vehicles'}, {'$set': {'seq': 0}}, upsert=True)
    for v in EXPANDED_VEHICLES:
        vid = get_next_id('vehicles')
        db.vehicles.insert_one({
            'id': vid,
            'name': v['name'],
            'plate': v.get('plate', f'41 LOG {vid:03d}'),
            'type': v.get('type', 'truck'),
            'category': v.get('category', 'Lojistik'),
            'capacity': int(v['capacity']),
            'volume_m3': float(v.get('volume_m3', 10.0)),
            'rental_cost': float(v.get('rental_cost', 0.0)),
            'fuel_type': v.get('fuel_type', 'diesel'),
            'fuel_liters_per_100km': float(v.get('fuel_liters_per_100km', 10.0)),
            'fuel_consumption': float(v['fuel_consumption']),
            'co2_g_per_km': float(v.get('co2_g_per_km', 250.0)),
            'speed_factor': float(v.get('speed_factor', 1.0)),
            'icon': v.get('icon', 'fa-truck'),
            'color': v.get('color', '#6366f1'),
            'description': v.get('description', ''),
            'is_owned': int(v.get('is_owned', 1))
        })
    print(f"  [+] {len(EXPANDED_VEHICLES)} adet çok sınıflı lojistik araç filosu eklendi.")

    # 5. Gerçekçi Türkiye Akaryakıt & Operasyonel Maliyet Parametreleri
    db.parameters.delete_many({})
    db.parameters.insert_one({
        'id': 1,
        'cost_per_km': 10.5,
        'rental_cost': 650.0,
        'rental_capacity': 1000,
        'fuel_prices': LOGISTICS_PARAMS.get('fuel_prices', {
            'diesel_per_liter': 92.50,
            'gasoline_per_liter': 85.50,
            'adblue_per_liter': 36.50,
            'lpg_per_liter': 45.00
        }),
        'toll_rates': LOGISTICS_PARAMS.get('toll_rates', {
            'osmangazi_bridge': 980.0,
            'canakkale_1915': 740.0,
            'yavuz_sultan_selim': 180.0,
            'highway_per_km': 1.80
        }),
        'driver_daily_wage': 2500.0,
        'co2_emission_factors': {
            'diesel': 2.68,
            'gasoline': 2.31
        }
    })
    print("  [+] Gerçekçi akaryakıt ve lojistik maliyet parametreleri yüklendi.")
    print("  [+] Sistem parametreleri kaydedildi.")

    print("[OK] MongoDB veritabanı başarıyla hazırlandı!")
    return True
