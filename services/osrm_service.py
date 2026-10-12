# -*- coding: utf-8 -*-
"""
OSRM (Open Source Routing Machine) Harita & Rota Servisi
Gerçek karayolu geometrisi, mesafe ve süre verilerini çeker.
"""
import json
import urllib.request
from typing import Dict, List, Optional, Tuple


def get_route_geometry(coordinates: List[Tuple[float, float]]) -> Optional[Dict]:
    """
    Verilen istasyon koordinatları için OSRM API üzerinden gerçek karayolu rotasını döner.
    
    :param coordinates: [(latitude, longitude), ...] tuple listesi
    :return: {'geometry': GeoJSON, 'distance': float (km), 'duration': float (dk)} veya None
    """
    if not coordinates or len(coordinates) < 2:
        return None

    try:
        # DÜZELTME: OSRM standardı {longitude},{latitude} sıralaması bekler!
        coords_str = ";".join([f"{lon:.6f},{lat:.6f}" for lat, lon in coordinates])
        url = f"http://router.project-osrm.org/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'LogiRoute Logistics Platform/2.0 (contact: info@logiroute.local)'
            }
        )
        
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('code') == 'Ok' and data.get('routes'):
                best_route = data['routes'][0]
                return {
                    'geometry': best_route['geometry'],
                    'distance': round(best_route['distance'] / 1000.0, 2),
                    'duration': round(best_route['duration'] / 60.0, 1)
                }
    except Exception as e:
        print(f"[!] OSRM Geometri Servis Uyarısı: {e}. Yerel düz geometri fallback kullanılıyor.")

    # OSRM çevrimdışıysa veya erişilemezse Leaflet için yedek GeoJSON LineString üret
    return {
        'geometry': {
            'type': 'LineString',
            'coordinates': [[lon, lat] for lat, lon in coordinates]
        },
        'distance': 0.0,
        'duration': 0.0,
        'fallback': True
    }
