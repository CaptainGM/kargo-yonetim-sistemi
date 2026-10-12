# -*- coding: utf-8 -*-
"""
İstasyon Yönetimi HTTP İşleyicileri
"""
from typing import Dict
from database import get_db, get_next_id, serialize_docs
from handlers.base_handler import BaseHandler


def handle_get_stations(handler):
    db = get_db()
    stations = list(db.stations.find({'is_active': 1}).sort('name', 1))
    BaseHandler.send_json(handler, serialize_docs(stations))


def handle_add_station(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    name = data.get('name', '').strip()
    try:
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
    except (ValueError, TypeError):
        BaseHandler.send_json(handler, {'error': 'Geçersiz koordinatlar'}, 400)
        return

    if not name:
        BaseHandler.send_json(handler, {'error': 'İstasyon adı gerekli'}, 400)
        return

    db = get_db()
    if db.stations.find_one({'name': name}):
        BaseHandler.send_json(handler, {'error': 'Bu istasyon adı zaten mevcut'}, 400)
        return

    sid = get_next_id('stations')
    is_depot = bool(data.get('is_depot')) or ('depo' in name.lower() or 'hub' in name.lower())
    city = data.get('city', '').strip()
    district = data.get('district', '').strip()
    db.stations.insert_one({
        'id': sid,
        'name': name,
        'city': city,
        'district': district,
        'latitude': latitude,
        'longitude': longitude,
        'is_active': 1,
        'is_depot': is_depot
    })

    BaseHandler.send_json(handler, {'success': True, 'id': sid})


def handle_delete_station(handler, station_id: int):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    db = get_db()
    station = db.stations.find_one({'id': station_id})
    if station and station.get('is_depot'):
        BaseHandler.send_json(handler, {'error': 'Merkez depo silinemez!'}, 400)
        return

    db.stations.delete_one({'id': station_id})
    db.cargos.delete_many({'station_id': station_id})
    BaseHandler.send_json(handler, {'success': True})
