# -*- coding: utf-8 -*-
"""
Yönetim, Parametreler, Kullanıcılar ve Veritabanı Görüntüleyici HTTP İşleyicileri
"""
from typing import Dict
from database import get_db, serialize_doc, serialize_docs
from handlers.base_handler import BaseHandler


def handle_get_parameters(handler):
    db = get_db()
    params = db.parameters.find_one({'id': 1}) or {
        'cost_per_km': 1.0,
        'rental_cost': 200.0,
        'rental_capacity': 500
    }
    BaseHandler.send_json(handler, serialize_doc(params))


def handle_update_parameters(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    try:
        cost_per_km = float(data.get('cost_per_km', 1.0))
        rental_cost = float(data.get('rental_cost', 200.0))
        rental_capacity = int(data.get('rental_capacity', 500))
    except (ValueError, TypeError):
        BaseHandler.send_json(handler, {'error': 'Geçersiz parametre değerleri'}, 400)
        return

    db = get_db()
    db.parameters.update_one(
        {'id': 1},
        {'$set': {
            'cost_per_km': cost_per_km,
            'rental_cost': rental_cost,
            'rental_capacity': rental_capacity
        }},
        upsert=True
    )
    BaseHandler.send_json(handler, {'success': True})


def handle_get_stats(handler):
    """Dashboard özet istatistiklerini ve Chart.js grafik verilerini döner."""
    db = get_db()
    total_cargos = db.cargos.count_documents({})
    pending_cargos = db.cargos.count_documents({'status': 'pending'})
    assigned_cargos = db.cargos.count_documents({'status': 'assigned'})
    total_stations = db.stations.count_documents({'is_active': 1})
    total_vehicles = db.vehicles.count_documents({'is_owned': 1})
    total_routes = db.routes.count_documents({})

    # Toplam ağırlık
    all_cargos = list(db.cargos.find())
    total_weight = sum(c.get('weight', 0) for c in all_cargos)

    # Rota maliyetleri
    all_routes = list(db.routes.find())
    total_cost = sum(r.get('total_cost', 0) for r in all_routes)
    total_distance = sum(r.get('total_distance', 0) for r in all_routes)

    # İstasyonlara göre kargo dağılımı (Grafik için)
    stations = list(db.stations.find({'is_active': 1}))
    station_names = [s['name'] for s in stations]
    station_cargo_counts = []
    for s in stations:
        cnt = db.cargos.count_documents({'station_id': s['id']})
        station_cargo_counts.append(cnt)

    BaseHandler.send_json(handler, {
        'total_cargos': total_cargos,
        'pending_cargos': pending_cargos,
        'assigned_cargos': assigned_cargos,
        'total_stations': total_stations,
        'total_vehicles': total_vehicles,
        'total_routes': total_routes,
        'total_weight': round(total_weight, 2),
        'total_cost': round(total_cost, 2),
        'total_distance': round(total_distance, 2),
        'charts': {
            'station_labels': station_names,
            'station_counts': station_cargo_counts,
            'status_labels': ['Bekleyen', 'Atanmış'],
            'status_counts': [pending_cargos, assigned_cargos]
        }
    })


def handle_get_db_stats(handler):
    db = get_db()
    BaseHandler.send_json(handler, {
        'users_count': db.users.count_documents({}),
        'stations_count': db.stations.count_documents({}),
        'vehicles_count': db.vehicles.count_documents({}),
        'cargos_count': db.cargos.count_documents({}),
        'routes_count': db.routes.count_documents({}),
        'db_engine': 'MongoDB',
        'db_name': db.name
    })


def handle_get_db_data(handler):
    """
    /db-view sayfası için tüm MongoDB koleksiyonlarındaki belgeleri döner.
    """
    db = get_db()
    data = {
        'success': True,
        'users': serialize_docs(list(db.users.find())),
        'stations': serialize_docs(list(db.stations.find().sort('name', 1))),
        'vehicles': serialize_docs(list(db.vehicles.find())),
        'cargos': serialize_docs(list(db.cargos.find().sort('id', -1))),
        'routes': serialize_docs(list(db.routes.find().sort('created_at', -1))),
        'parameters': serialize_docs(list(db.parameters.find())),
        'password_reset_codes': serialize_docs(list(db.password_reset_codes.find().sort('created_at', -1)))
    }
    BaseHandler.send_json(handler, data)


def handle_get_users(handler):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    users = list(db.users.find({}, {'password': 0}).sort('id', 1))
    BaseHandler.send_json(handler, serialize_docs(users))


def handle_delete_user(handler, user_id: int):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    user = db.users.find_one({'id': user_id})
    if user and user.get('role') == 'admin':
        BaseHandler.send_json(handler, {'error': 'Yönetici hesabı silinemez'}, 400)
        return
    db.users.delete_one({'id': user_id})
    db.cargos.delete_many({'user_id': user_id})
    BaseHandler.send_json(handler, {'success': True})


def handle_get_reset_codes(handler):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return
    db = get_db()
    codes = list(db.password_reset_codes.find().sort('created_at', -1).limit(50))
    BaseHandler.send_json(handler, serialize_docs(codes))
