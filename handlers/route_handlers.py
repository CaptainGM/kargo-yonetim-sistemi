# -*- coding: utf-8 -*-
"""
Rota Görüntüleme, Silme ve OSRM Geometri HTTP İşleyicileri
"""
from typing import Dict
from database import get_db, serialize_docs
from handlers.base_handler import BaseHandler
from services.osrm_service import get_route_geometry


def handle_get_routes(handler):
    db = get_db()
    routes = list(db.routes.find().sort('created_at', -1))
    BaseHandler.send_json(handler, serialize_docs(routes))


def handle_delete_route(handler, route_id: int):
    session = BaseHandler.get_session(handler)
    if not session or session.get('role') != 'admin':
        BaseHandler.send_json(handler, {'error': 'Yetkiniz yok'}, 403)
        return

    db = get_db()
    route = db.routes.find_one({'id': route_id})
    if route:
        cargo_ids = route.get('cargo_ids', [])
        if cargo_ids:
            # Kargoları tekrar 'pending' durumuna al
            db.cargos.update_many(
                {'id': {'$in': cargo_ids}},
                {'$set': {'status': 'pending', 'route_id': None}}
            )
        db.routes.delete_one({'id': route_id})

    BaseHandler.send_json(handler, {'success': True})


def handle_route_geometry(handler, data: Dict):
    """
    İstasyon adları listesini alarak OSRM üzerinden gerçek karayolu koordinat geometrisini döner.
    """
    route_station_names = data.get('stations', [])
    if len(route_station_names) < 2:
        BaseHandler.send_json(handler, {'error': 'En az 2 istasyon gerekli'}, 400)
        return

    db = get_db()
    coordinates = []

    for name in route_station_names:
        st = db.stations.find_one({'name': name})
        if st and 'latitude' in st and 'longitude' in st:
            coordinates.append((float(st['latitude']), float(st['longitude'])))

    if len(coordinates) < 2:
        BaseHandler.send_json(handler, {'error': 'İstasyon koordinatları bulunamadı'}, 400)
        return

    geom_result = get_route_geometry(coordinates)
    if geom_result:
        BaseHandler.send_json(handler, geom_result)
    else:
        BaseHandler.send_json(handler, {'error': 'Rota geometrisi hesaplanamadı'}, 500)
