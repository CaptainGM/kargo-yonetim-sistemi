# -*- coding: utf-8 -*-
"""
Araç Filosu Yönetimi HTTP İşleyicileri
"""
from typing import Dict
from database import get_db, get_next_id, serialize_docs
from handlers.base_handler import BaseHandler


def handle_get_vehicles(handler):
    db = get_db()
    vehicles = list(db.vehicles.find({'is_owned': 1}).sort('capacity', 1))
    BaseHandler.send_json(handler, serialize_docs(vehicles))


def handle_add_vehicle(handler, data: Dict):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    name = data.get('name', '').strip()
    try:
        capacity = int(data.get('capacity', 0))
        rental_cost = float(data.get('rental_cost', 0))
        fuel_consumption = float(data.get('fuel_consumption', 0.1))
        is_owned = int(data.get('is_owned', 1))
    except (ValueError, TypeError):
        BaseHandler.send_json(handler, {'error': 'Geçersiz araç parametreleri'}, 400)
        return

    if not name or capacity <= 0:
        BaseHandler.send_json(handler, {'error': 'Araç adı ve geçerli bir kapasite gerekli'}, 400)
        return

    db = get_db()
    vid = get_next_id('vehicles')
    db.vehicles.insert_one({
        'id': vid,
        'name': name,
        'type': data.get('type', 'truck'),
        'category': data.get('category', 'Lojistik'),
        'capacity': capacity,
        'volume_m3': float(data.get('volume_m3', 10.0)),
        'rental_cost': rental_cost,
        'fuel_consumption': fuel_consumption,
        'speed_factor': float(data.get('speed_factor', 1.0)),
        'icon': data.get('icon', 'fa-truck'),
        'color': data.get('color', '#6366f1'),
        'description': data.get('description', ''),
        'is_owned': is_owned
    })

    BaseHandler.send_json(handler, {'success': True, 'id': vid})


def handle_delete_vehicle(handler, vehicle_id: int):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    db = get_db()
    db.vehicles.delete_one({'id': vehicle_id})
    BaseHandler.send_json(handler, {'success': True})
