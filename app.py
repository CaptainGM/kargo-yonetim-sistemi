# -*- coding: utf-8 -*-

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import hashlib
import math
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.request

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': '',  
    'database': os.environ.get('DB_NAME', 'kargo_sistemi'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}


DB_CONFIG['password'] = os.environ.get('DB_PASSWORD', '')

EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', 587)),
    'sender_email': os.environ.get('SENDER_EMAIL', ''),
    'sender_password': os.environ.get('SENDER_PASSWORD', ''),
    'sender_name': 'Kargo İşletme Sistemi'
}

sessions: Dict[str, Dict] = {}


def get_db():
    try:
        conn = mysql.connector.connect(
            **DB_CONFIG,
            connection_timeout=30,
            autocommit=False,
            use_pure=True,
            pool_reset_session=False
        )
        return conn
    except Error as e:
        print(f"MySQL Bağlantı Hatası: {e}")
        import traceback
        traceback.print_exc()
        return None


def init_database():
    # Bağlantı bilgilerini göster
    print(f"MySQL Bağlantı Denemesi:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG.get('port', 3307)}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Password: {'(boş)' if not DB_CONFIG.get('password') else '***'}")
    print(f"  Database: {DB_CONFIG['database']}")
    print()
    
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG.get('port', 3307),
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            connection_timeout=5
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255) NOT NULL,
            plain_password VARCHAR(100),
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(255) UNIQUE AFTER username")
        except Exception:
            pass
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN plain_password VARCHAR(100) AFTER password")
        except Exception:
            pass
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS password_reset_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            code VARCHAR(6) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL,
            used TINYINT DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS stations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            latitude DOUBLE NOT NULL,
            longitude DOUBLE NOT NULL,
            is_active TINYINT DEFAULT 1
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            capacity INT NOT NULL,
            rental_cost DOUBLE DEFAULT 0,
            fuel_consumption DOUBLE DEFAULT 0.1,
            is_owned TINYINT DEFAULT 1
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS cargos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            station_id INT,
            weight DOUBLE NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            delivery_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS routes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_id INT,
            route_data TEXT,
            total_distance DOUBLE,
            total_cost DOUBLE,
            total_weight DOUBLE,
            cargo_count INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS route_cargos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            route_id INT,
            cargo_id INT,
            FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
            FOREIGN KEY (cargo_id) REFERENCES cargos(id) ON DELETE CASCADE
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS parameters (
            id INT PRIMARY KEY,
            cost_per_km DOUBLE DEFAULT 1.0,
            rental_cost DOUBLE DEFAULT 200.0,
            rental_capacity INT DEFAULT 500
        )''')
        
        conn.commit()
        insert_default_data(cursor, conn)
        
        try:
            cursor.execute("UPDATE users SET plain_password='admin123' WHERE username='admin' AND plain_password IS NULL")
            cursor.execute("UPDATE users SET plain_password='user123' WHERE username='user' AND plain_password IS NULL")
            conn.commit()
        except Exception:
            pass
        
        cursor.close()
        conn.close()
        print("[OK] Veritabani basariyla olusturuldu!")
        return True
        
    except Error as e:
        err_msg = str(e)
        print(f"Veritabanı oluşturma hatası: {err_msg}")
        
        if 'Access denied' in err_msg:
            print("\n[ÇÖZÜM]")
            print("XAMPP MariaDB boş şifre kullanıyor.")
            print("start.bat dosyasında şu satırı bulun:")
            print('  set "DB_PASSWORD="')
            print("ve şu şekilde değiştirin:")
            print('  set "DB_PASSWORD=mysql_sifreniz"')
            print("\nVeya start.bat dosyasını yeniden oluşturun.")
        
        return False


def insert_default_data(cursor, conn):
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        cursor.execute("INSERT IGNORE INTO users (username, password, plain_password, role) VALUES (%s, %s, %s, %s)", ('admin', admin_pass, 'admin123', 'admin'))
    except Exception:
        pass
    
    user_pass = hashlib.sha256('user123'.encode()).hexdigest()
    try:
        cursor.execute("INSERT IGNORE INTO users (username, password, plain_password, role) VALUES (%s, %s, %s, %s)", ('user', user_pass, 'user123', 'user'))
    except Exception:
        pass
    
    districts = [
        ('Umuttepe Kampüsü (KOÜ)', 40.8225, 29.9213),
        ('Başiskele', 40.714025, 29.928362), ('Çayırova', 40.8261, 29.3711),
        ('Darıca', 40.7692, 29.3753), ('Derince', 40.7550, 29.8314),
        ('Dilovası', 40.7833, 29.5333), ('Gebze', 40.8027, 29.4307),
        ('Gölcük', 40.72, 29.82), ('Kandıra', 41.0711, 30.1528),
        ('Karamürsel', 40.6917, 29.6167), ('Kartepe', 40.7533, 30.0224),
        ('Körfez', 40.762527, 29.777346), ('İzmit', 40.7654, 29.9408)
    ]
    
    for name, lat, lon in districts:
        try:
            cursor.execute("INSERT IGNORE INTO stations (name, latitude, longitude) VALUES (%s, %s, %s)", (name, lat, lon))
        except Exception:
            pass
    
    vehicles = [
        ('Araç 1 (500kg)', 500, 0, 0.08, 1),
        ('Araç 2 (750kg)', 750, 0, 0.10, 1),
        ('Araç 3 (1000kg)', 1000, 0, 0.12, 1)
    ]
    
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    if cursor.fetchone()[0] == 0:
        for name, cap, cost, fuel, owned in vehicles:
            cursor.execute("INSERT INTO vehicles (name, capacity, rental_cost, fuel_consumption, is_owned) VALUES (%s, %s, %s, %s, %s)", (name, cap, cost, fuel, owned))
    




def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_route_geometry(coordinates: List) -> Optional[Dict]:
    try:
        coords_str = ";".join([f"{lat},{lon}" for lat, lon in coordinates])
        url = f"http://router.project-osrm.org/route/v1/driving/{coords_str}?overview=full&geometries=geojson"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data['code'] == 'Ok':
                return {
                    'geometry': data['routes'][0]['geometry'],
                    'distance': data['routes'][0]['distance'] / 1000,
                    'duration': data['routes'][0]['duration'] / 60
                }
    except Exception as e:
        print(f"OSRM Error: {e}")
    return None

def dict_from_row(cursor, row) -> Dict:
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

class RouteOptimizer:
    def __init__(self, stations: List[Dict], cargos: List[Dict], vehicles: List[Dict], params: Dict, optimize_for: str = 'balanced'):
        self.stations: Dict[int, Dict] = {s['id']: s for s in stations}
        self.cargos = cargos
        self.vehicles = sorted(vehicles, key=lambda v: v['capacity'], reverse=True)
        self.params = params
        self.optimize_for = optimize_for
        self.depot: Optional[Dict] = None
        
        for s in stations:
            name_lower = s['name'].lower()
            if 'umuttepe' in name_lower or 'koü' in name_lower or 'kou' in name_lower or 'kampüs' in name_lower:
                self.depot = s
                break
        if not self.depot:
            self.depot = {
                'id': -1,
                'name': 'Umuttepe Kampüsü (KOÜ)',
                'latitude': 40.8225,
                'longitude': 29.9213
            }
            self.stations[-1] = self.depot
    
    def get_real_road_distance(self, name1: str, name2: str) -> float:
        n1 = name1.lower().replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g')
        n2 = name2.lower().replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ç', 'c').replace('ğ', 'g')
        
        distances = {
            ('umuttepe', 'izmit'): 5,
            ('umuttepe', 'derince'): 8,
            ('umuttepe', 'korfez'): 15,
            ('umuttepe', 'gebze'): 45,
            ('umuttepe', 'cayirova'): 50,
            ('umuttepe', 'darica'): 55,
            ('umuttepe', 'dilovasi'): 35,
            ('umuttepe', 'basiskele'): 12,
            ('umuttepe', 'golcuk'): 18,
            ('umuttepe', 'karamursel'): 35,
            ('umuttepe', 'kartepe'): 20,
            ('umuttepe', 'kandira'): 45,
            
            ('izmit', 'derince'): 6,
            ('izmit', 'korfez'): 12,
            ('izmit', 'gebze'): 42,
            ('izmit', 'cayirova'): 48,
            ('izmit', 'darica'): 52,
            ('izmit', 'dilovasi'): 32,
            ('izmit', 'basiskele'): 10,
            ('izmit', 'golcuk'): 15,
            ('izmit', 'karamursel'): 32,
            ('izmit', 'kartepe'): 18,
            ('izmit', 'kandira'): 50,
            
            ('derince', 'korfez'): 8,
            ('derince', 'gebze'): 38,
            ('derince', 'cayirova'): 44,
            ('derince', 'darica'): 48,
            ('derince', 'dilovasi'): 28,
            ('derince', 'basiskele'): 15,
            ('derince', 'golcuk'): 20,
            ('derince', 'karamursel'): 38,
            ('derince', 'kartepe'): 22,
            ('derince', 'kandira'): 55,
            
            ('korfez', 'gebze'): 30,
            ('korfez', 'cayirova'): 36,
            ('korfez', 'darica'): 40,
            ('korfez', 'dilovasi'): 20,
            ('korfez', 'basiskele'): 22,
            ('korfez', 'golcuk'): 28,
            ('korfez', 'karamursel'): 45,
            ('korfez', 'kartepe'): 30,
            ('korfez', 'kandira'): 60,
            
            ('gebze', 'cayirova'): 8,
            ('gebze', 'darica'): 12,
            ('gebze', 'dilovasi'): 12,
            ('gebze', 'basiskele'): 52,
            ('gebze', 'golcuk'): 58,
            ('gebze', 'karamursel'): 55,
            ('gebze', 'kartepe'): 60,
            ('gebze', 'kandira'): 90,
            
            ('cayirova', 'darica'): 5,
            ('cayirova', 'dilovasi'): 18,
            ('cayirova', 'basiskele'): 58,
            ('cayirova', 'golcuk'): 64,
            ('cayirova', 'karamursel'): 60,
            ('cayirova', 'kartepe'): 68,
            ('cayirova', 'kandira'): 95,
            
            ('darica', 'dilovasi'): 22,
            ('darica', 'basiskele'): 62,
            ('darica', 'golcuk'): 68,
            ('darica', 'karamursel'): 65,
            ('darica', 'kartepe'): 72,
            ('darica', 'kandira'): 100,
            
            ('dilovasi', 'basiskele'): 42,
            ('dilovasi', 'golcuk'): 48,
            ('dilovasi', 'karamursel'): 45,
            ('dilovasi', 'kartepe'): 50,
            ('dilovasi', 'kandira'): 80,
            
            ('basiskele', 'golcuk'): 8,
            ('basiskele', 'karamursel'): 25,
            ('basiskele', 'kartepe'): 15,
            ('basiskele', 'kandira'): 55,
            
            ('golcuk', 'karamursel'): 18,
            ('golcuk', 'kartepe'): 22,
            ('golcuk', 'kandira'): 60,
            
            ('karamursel', 'kartepe'): 40,
            ('karamursel', 'kandira'): 75,
            
            ('kartepe', 'kandira'): 40,
        }
        
        key1 = (n1, n2)
        key2 = (n2, n1)
        
        for key in [key1, key2]:
            for dist_key, dist_val in distances.items():
                k1, k2 = dist_key
                if (k1 in key[0] or key[0] in k1) and (k2 in key[1] or key[1] in k2):
                    return float(dist_val)
                if (k1 in key[1] or key[1] in k1) and (k2 in key[0] or key[0] in k2):
                    return float(dist_val)
        
        return 0.0
    
    def calculate_distance_matrix(self) -> Dict[int, Dict[int, float]]:
        station_ids = list(self.stations.keys())
        matrix: Dict[int, Dict[int, float]] = {}
        
        for i in station_ids:
            matrix[i] = {}
            for j in station_ids:
                if i == j:
                    matrix[i][j] = 0
                else:
                    s1, s2 = self.stations[i], self.stations[j]
                    name1 = s1.get('name', '')
                    name2 = s2.get('name', '')
                    
                    real_dist = self.get_real_road_distance(name1, name2)
                    
                    if real_dist:
                        matrix[i][j] = real_dist
                    else:
                        base_dist = haversine(s1['latitude'], s1['longitude'], s2['latitude'], s2['longitude'])
                        matrix[i][j] = base_dist * 1.3
        
        return matrix
    
    def greedy_route(self, available_cargos: List[Dict], capacity: int, vehicle: Optional[Dict] = None, start_station_id: Optional[int] = None):
        if not available_cargos:
                return [], [], 0, 0
        
        dist_matrix = self.calculate_distance_matrix()
        depot_id = self.depot['id'] if self.depot else None
        
        cargos_with_info = []
        for cargo in available_cargos:
            station_id = cargo['station_id']
            dist_to_depot = dist_matrix.get(station_id, {}).get(depot_id, 100) if depot_id else 100
            cargos_with_info.append({
                **cargo,
                'dist_to_depot': dist_to_depot
            })
        
        selected_cargos: List[Dict] = []
        current_weight = 0
        selected_station_ids = set()
        selected_ids = set()
        
        if self.optimize_for == 'max_count':
            
            sorted_by_weight = sorted(cargos_with_info, key=lambda c: c['weight'])
            
            remaining_capacity = capacity
            for cargo in sorted_by_weight:
                if cargo['weight'] <= remaining_capacity:
                    selected_cargos.append(cargo)
                    current_weight += cargo['weight']
                    remaining_capacity -= cargo['weight']
                    selected_station_ids.add(cargo['station_id'])
                    selected_ids.add(cargo['id'])
            
            for cargo in sorted_by_weight:
                if cargo['id'] not in selected_ids:
                    if cargo['weight'] <= remaining_capacity:
                        selected_cargos.append(cargo)
                        current_weight += cargo['weight']
                        remaining_capacity -= cargo['weight']
                        selected_station_ids.add(cargo['station_id'])
                        selected_ids.add(cargo['id'])
                    
        elif self.optimize_for == 'max_weight':
            sorted_by_weight = sorted(cargos_with_info, key=lambda c: c['weight'], reverse=True)
            remaining_cargos = []
            
            for cargo in sorted_by_weight:
                if current_weight + cargo['weight'] <= capacity:
                    selected_cargos.append(cargo)
                    current_weight += cargo['weight']
                    selected_station_ids.add(cargo['station_id'])
                else:
                    remaining_cargos.append(cargo)
            
            remaining_cargos.sort(key=lambda c: c['weight'])
            for cargo in remaining_cargos:
                if current_weight + cargo['weight'] <= capacity:
                    selected_cargos.append(cargo)
                    current_weight += cargo['weight']
                    selected_station_ids.add(cargo['station_id'])
                    
        else:
            sorted_cargos = sorted(cargos_with_info, key=lambda c: c['dist_to_depot'])
            for cargo in sorted_cargos:
                if current_weight + cargo['weight'] <= capacity:
                    selected_cargos.append(cargo)
                    current_weight += cargo['weight']
                    selected_station_ids.add(cargo['station_id'])
                    selected_ids.add(cargo['id'])
            
            for cargo in sorted_cargos:
                if cargo['id'] not in selected_ids:
                    if current_weight + cargo['weight'] <= capacity:
                        selected_cargos.append(cargo)
                        current_weight += cargo['weight']
                        selected_station_ids.add(cargo['station_id'])
        
        if not selected_cargos:
            return [], [], 0, 0
        
        station_list = list(selected_station_ids)
        depot_id_int = depot_id if depot_id is not None else -1
        route = self.optimize_route_order(station_list, depot_id_int, dist_matrix)
        
        if len(route) > 3:
            route = self.two_opt(route)
        
        distance = 0.0
        for i in range(len(route) - 1):
            distance += dist_matrix.get(route[i], {}).get(route[i+1], 0)
        
        if depot_id and (not route or route[-1] != depot_id):
            if route:
                distance += dist_matrix.get(route[-1], {}).get(depot_id, 0)
            route.append(depot_id)
        
        cost = distance * self.params['cost_per_km']
        
        return route, selected_cargos, distance, cost
    
    def optimize_route_order(self, station_ids: List[int], depot_id: int, dist_matrix: Dict) -> List[int]:
        if not station_ids:
            return []
        
        if len(station_ids) == 1:
            return station_ids[:]
        
        def build_nn_route(start_id: int, all_ids: List[int]) -> tuple:
            route = [start_id]
            remaining = set(all_ids) - {start_id}
            total_dist = 0.0
            
            while remaining:
                current = route[-1]
                nearest = None
                nearest_dist = float('inf')
                
                for sid in remaining:
                    dist = dist_matrix.get(current, {}).get(sid, float('inf'))
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest = sid
                
                if nearest:
                    total_dist += nearest_dist
                    route.append(nearest)
                    remaining.remove(nearest)
                else:
                    break
            
            if route:
                total_dist += dist_matrix.get(route[-1], {}).get(depot_id, 0)
            
            return route, total_dist
        
        best_route = None
        best_dist = float('inf')
        
        for start_id in station_ids:
            route, total_dist = build_nn_route(start_id, station_ids)
            if total_dist < best_dist:
                best_dist = total_dist
                best_route = route
        
        return best_route if best_route else station_ids[:]
    
    def two_opt(self, route: List[int]) -> List[int]:
        if len(route) < 4:
            return route
        
        dist_matrix = self.calculate_distance_matrix()
        route = route[:]
        improved = True
        max_iterations = 200
        iteration = 0
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            best_delta = 0
            best_i = -1
            best_j = -1
            
            for i in range(len(route) - 2):
                for j in range(i + 2, len(route)):
                    if j == len(route) - 1 and i == 0:
                        continue
                    
                    d1 = dist_matrix.get(route[i], {}).get(route[i+1], 0)
                    if j + 1 < len(route):
                        d2 = dist_matrix.get(route[j], {}).get(route[j+1], 0)
                    else:
                        d2 = 0
                    
                    d3 = dist_matrix.get(route[i], {}).get(route[j], 0)
                    if j + 1 < len(route):
                        d4 = dist_matrix.get(route[i+1], {}).get(route[j+1], 0)
                    else:
                        d4 = 0
                    
                    delta = (d3 + d4) - (d1 + d2)
                    
                    if delta < best_delta - 0.01:
                        best_delta = delta
                        best_i = i
                        best_j = j
            
            if best_i >= 0 and best_j >= 0:
                route[best_i+1:best_j+1] = list(reversed(route[best_i+1:best_j+1]))
                improved = True
        
        return route
    
    def solve_limited_vehicles(self) -> Dict:
        dist_matrix = self.calculate_distance_matrix()
        depot_id = self.depot['id'] if self.depot else None
        
        return self._optimal_bin_packing(dist_matrix, depot_id)
    
    def _optimal_bin_packing(self, dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        owned_vehicles = sorted([v for v in self.vehicles if v['is_owned']], 
                                key=lambda v: v['capacity'], reverse=True)
        all_cargos = list(self.cargos)
        
        if not all_cargos or not owned_vehicles:
            return self._empty_result(all_cargos)
        
        total_cargo_weight = sum(c['weight'] for c in all_cargos)
        
        for vehicle in owned_vehicles:
            if vehicle['capacity'] >= total_cargo_weight:
                result = self._build_route_result(vehicle, all_cargos, dist_matrix, depot_id)
                if result:
                    return {
                        'routes': [result],
                        'total_cost': round(result['cost'], 2),
                        'total_fuel_cost': round(result['fuel_cost'], 2),
                        'total_cargos': result['cargo_count'],
                        'total_weight': round(result['weight'], 2),
                        'undelivered': [],
                        'undelivered_details': [],
                        'optimize_for': self.optimize_for
                    }
        
        n_cargos = len(all_cargos)
        vehicle_caps = {v['id']: v['capacity'] for v in owned_vehicles}
        
        best_assignment = None
        best_count = -1
        best_weight = -1
        
        sorted_cargos = sorted(all_cargos, key=lambda c: c['weight'], reverse=True)
        
        def backtrack(idx, assignment, weights):
            nonlocal best_assignment, best_count, best_weight
            if idx == n_cargos:
                count = sum(len(v) for v in assignment.values())
                weight = sum(weights.values())
                if count > best_count or (count == best_count and weight > best_weight):
                    best_count = count
                    best_weight = weight
                    best_assignment = {k: list(v) for k, v in assignment.items()}
                return
            cargo = sorted_cargos[idx]
            for vehicle in owned_vehicles:
                vid = vehicle['id']
                if weights[vid] + cargo['weight'] <= vehicle_caps[vid]:
                    assignment[vid].append(cargo)
                    weights[vid] += cargo['weight']
                    backtrack(idx + 1, assignment, weights)
                    assignment[vid].pop()
                    weights[vid] -= cargo['weight']
            backtrack(idx + 1, assignment, weights)
        
        if n_cargos <= 20:
            init_assign = {v['id']: [] for v in owned_vehicles}
            init_weights = {v['id']: 0.0 for v in owned_vehicles}
            backtrack(0, init_assign, init_weights)
        else:
            best_assignment = self._greedy_best_fit(sorted_cargos, owned_vehicles)
            best_count = sum(len(v) for v in best_assignment.values())
        
        if best_assignment is None:
            best_assignment = {v['id']: [] for v in owned_vehicles}
        
        return self._build_final_result(best_assignment, owned_vehicles, dist_matrix, depot_id)
    
    def _greedy_best_fit(self, cargos: List[Dict], vehicles: List[Dict]) -> Dict[int, List]:
        sorted_vehicles = sorted(vehicles, key=lambda v: v['capacity'], reverse=True)
        
        assignment = {v['id']: [] for v in vehicles}
        weights = {v['id']: 0.0 for v in vehicles}
        
        sorted_cargos = sorted(cargos, key=lambda c: c['weight'], reverse=True)
        
        for cargo in sorted_cargos:
            for v in sorted_vehicles:
                remaining = v['capacity'] - weights[v['id']]
                if cargo['weight'] <= remaining:
                    assignment[v['id']].append(cargo)
                    weights[v['id']] += cargo['weight']
                    break
        
        return assignment
    
    def _empty_result(self, cargos: List[Dict]) -> Dict:
        return {
            'routes': [],
            'total_cost': 0,
            'total_fuel_cost': 0,
            'total_cargos': 0,
            'total_weight': 0,
            'undelivered': cargos,
            'undelivered_details': [{'id': c['id'], 'weight': c['weight'], 
                                     'station_id': c['station_id'],
                                     'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')} 
                                    for c in cargos],
            'optimize_for': self.optimize_for
        }
    
    def _build_final_result(self, assignment: Dict[int, List], vehicles: List[Dict], 
                           dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        results = []
        total_cost = 0.0
        total_fuel_cost = 0.0
        assigned_ids = set()
        
        for vehicle in vehicles:
            cargos = assignment.get(vehicle['id'], [])
            if not cargos:
                continue
            
            for c in cargos:
                assigned_ids.add(c['id'])
            
            result = self._build_route_result(vehicle, cargos, dist_matrix, depot_id)
            if result:
                results.append(result)
                total_cost += result['cost']
                total_fuel_cost += result['fuel_cost']
        
        remaining = [c for c in self.cargos if c['id'] not in assigned_ids]
        undelivered_details = []
        for cargo in remaining:
            station_name = self.stations.get(cargo['station_id'], {}).get('name', 'Bilinmiyor')
            undelivered_details.append({
                'id': cargo['id'],
                'weight': cargo['weight'],
                'station_id': cargo['station_id'],
                'station_name': station_name
            })
        
        return {
            'routes': results,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_cargos': sum(r['cargo_count'] for r in results),
            'total_weight': round(sum(r['weight'] for r in results), 2),
            'undelivered': remaining,
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }
    
    def _knapsack_max_count(self, cargos: List[Dict], capacity: float) -> List[Dict]:
        if not cargos:
            return []
        
        n = len(cargos)
        
        int_capacity = int(capacity * 10)
        int_weights = [int(c['weight'] * 10) for c in cargos]
        
        INF = float('inf')
        dp = [(-1, INF, []) for _ in range(int_capacity + 1)]
        dp[0] = (0, 0, [])
        
        for i in range(n):
            w = int_weights[i]
            for cap in range(int_capacity, w - 1, -1):
                prev_count, prev_weight, prev_list = dp[cap - w]
                if prev_count >= 0:
                    new_count = prev_count + 1
                    new_weight = prev_weight + w
                    cur_count, cur_weight, _ = dp[cap]
                    if new_count > cur_count or (new_count == cur_count and new_weight < cur_weight):
                        dp[cap] = (new_count, new_weight, prev_list + [i])
        
        best_count = -1
        best_weight = INF
        best_indices = []
        
        for cap in range(int_capacity + 1):
            count, weight, indices = dp[cap]
            if count > best_count or (count == best_count and weight < best_weight):
                best_count = count
                best_weight = weight
                best_indices = indices
        
        return [cargos[i] for i in best_indices]
    
    def _knapsack_max_weight(self, cargos: List[Dict], capacity: float) -> List[Dict]:
        if not cargos:
            return []
        
        n = len(cargos)
        
        int_capacity = int(capacity * 10)
        int_weights = [int(c['weight'] * 10) for c in cargos]
        
        dp = [(0, []) for _ in range(int_capacity + 1)]
        
        for i in range(n):
            w = int_weights[i]
            for cap in range(int_capacity, w - 1, -1):
                prev_weight, prev_list = dp[cap - w]
                new_weight = prev_weight + w
                cur_weight, _ = dp[cap]
                if new_weight > cur_weight:
                    dp[cap] = (new_weight, prev_list + [i])
        
        best_weight = 0
        best_indices = []
        
        for cap in range(int_capacity + 1):
            weight, indices = dp[cap]
            if weight > best_weight:
                best_weight = weight
                best_indices = indices
        
        return [cargos[i] for i in best_indices]
    
    def _build_route_result(self, vehicle: Dict, selected_cargos: List[Dict], 
                            dist_matrix: Dict, depot_id: Optional[int]) -> Optional[Dict]:
        if not selected_cargos:
            return None
        
        station_ids = list(set(c['station_id'] for c in selected_cargos))
        route = self.optimize_route_order(station_ids, depot_id if depot_id else -1, dist_matrix)
        
        if len(route) > 3:
            route = self.two_opt(route)
        
        distance = 0.0
        for i in range(len(route) - 1):
            distance += dist_matrix.get(route[i], {}).get(route[i+1], 0)
        
        if depot_id and route and route[-1] != depot_id:
            distance += dist_matrix.get(route[-1], {}).get(depot_id, 0)
            route.append(depot_id)
        
        cost = distance * self.params['cost_per_km']
        total_weight = sum(c['weight'] for c in selected_cargos)
        
        cargo_users = []
        for c in selected_cargos:
            if c.get('user_id'):
                cargo_users.append({
                    'cargo_id': c['id'], 
                    'user_id': c['user_id'], 
                    'username': c.get('username', 'Bilinmiyor'), 
                    'weight': c['weight'], 
                    'station': c.get('station_name', '')
                })
        
        station_cargo_details = []
        station_groups: Dict[int, List[Dict]] = {}
        for cargo in selected_cargos:
            sid = cargo['station_id']
            if sid not in station_groups:
                station_groups[sid] = []
            station_groups[sid].append(cargo)
        
        for sid, cargos_list in station_groups.items():
            station_name = self.stations.get(sid, {}).get('name', 'Bilinmiyor')
            station_weight = sum(c['weight'] for c in cargos_list)
            station_cargo_details.append({
                'station_id': sid,
                'name': station_name,
                'cargo_count': len(cargos_list),
                'weight': station_weight
            })
        
        return {
            'vehicle': vehicle,
            'route': route,
            'route_names': [self.stations[sid]['name'] for sid in route if sid in self.stations],
            'cargos': selected_cargos,
            'cargo_users': cargo_users,
            'distance': round(distance, 2),
            'fuel_cost': round(cost, 2),
            'cost': round(cost, 2),
            'weight': round(total_weight, 2),
            'cargo_count': len(selected_cargos),
            'station_cargo_details': station_cargo_details
        }
    
    def _solve_balanced_global(self, dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        owned_vehicles = sorted([v for v in self.vehicles if v['is_owned']], key=lambda v: v['capacity'], reverse=True)
        all_cargos = list(self.cargos)
        
        if not all_cargos or not owned_vehicles:
            return {
                'routes': [],
                'total_cost': 0,
                'total_fuel_cost': 0,
                'total_cargos': 0,
                'total_weight': 0,
                'undelivered': all_cargos,
                'undelivered_details': [{'id': c['id'], 'weight': c['weight'], 'station_id': c['station_id'], 
                                         'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')} 
                                        for c in all_cargos],
                'optimize_for': self.optimize_for
            }
        
        total_cargo_weight = sum(c['weight'] for c in all_cargos)
        for vehicle in owned_vehicles:
            if vehicle['capacity'] >= total_cargo_weight:
                route, selected, distance, cost = self.greedy_route(all_cargos, vehicle['capacity'], vehicle)
                if len(selected) == len(all_cargos):
                    result = self._build_route_result(vehicle, selected, dist_matrix, depot_id)
                    if result:
                        return {
                            'routes': [result],
                            'total_cost': round(result['cost'], 2),
                            'total_fuel_cost': round(result['fuel_cost'], 2),
                            'total_cargos': result['cargo_count'],
                            'total_weight': round(result['weight'], 2),
                            'undelivered': [],
                            'undelivered_details': [],
                            'optimize_for': self.optimize_for
                        }
        
        vehicle_caps = {v['id']: v['capacity'] for v in owned_vehicles}
        
        orderings = [
            sorted(all_cargos, key=lambda c: c['weight'], reverse=True),
            sorted(all_cargos, key=lambda c: c['weight']),
            sorted(all_cargos, key=lambda c: (c['station_id'], -c['weight'])),
            all_cargos,
        ]
        
        overall_best_assignment = None
        overall_best_count = -1
        overall_best_weight = -1
        
        for cargo_order in orderings:
            best_assignment = None
            best_count = -1
            best_weight = -1
            
            def backtrack(cargo_idx: int, current_assignment: Dict[int, List], current_weights: Dict[int, float]):
                nonlocal best_assignment, best_count, best_weight
                
                if cargo_idx == len(cargo_order):
                    total_count = sum(len(cargos) for cargos in current_assignment.values())
                    total_wt = sum(current_weights.values())
                    
                    if total_count > best_count or (total_count == best_count and total_wt > best_weight):
                        best_count = total_count
                        best_weight = total_wt
                        best_assignment = {vid: list(cargos) for vid, cargos in current_assignment.items()}
                    return
                
                cargo = cargo_order[cargo_idx]
                cargo_weight = cargo['weight']
                
                remaining_cargos_count = len(cargo_order) - cargo_idx
                current_count = sum(len(cargos) for cargos in current_assignment.values())
                if current_count + remaining_cargos_count <= best_count:
                    return
                
                tried_capacities = set()
                for vehicle in owned_vehicles:
                    vid = vehicle['id']
                    remaining_cap = vehicle_caps[vid] - current_weights[vid]
                    cap_key = round(remaining_cap, 2)
                    if cap_key in tried_capacities:
                        continue
                    
                    if cargo_weight <= remaining_cap:
                        tried_capacities.add(cap_key)
                        current_assignment[vid].append(cargo)
                        current_weights[vid] += cargo_weight
                        backtrack(cargo_idx + 1, current_assignment, current_weights)
                        current_assignment[vid].pop()
                        current_weights[vid] -= cargo_weight
                
                backtrack(cargo_idx + 1, current_assignment, current_weights)
            
            if len(cargo_order) > 18:
                assignment = self._heuristic_max_count_assignment(cargo_order, owned_vehicles)
                count = sum(len(c) for c in assignment.values())
                weight = sum(sum(cargo['weight'] for cargo in cargos) for cargos in assignment.values())
                if count > best_count or (count == best_count and weight > best_weight):
                    best_count = count
                    best_weight = weight
                    best_assignment = assignment
            else:
                initial_assignment = {v['id']: [] for v in owned_vehicles}
                initial_weights = {v['id']: 0.0 for v in owned_vehicles}
                backtrack(0, initial_assignment, initial_weights)
            
            if best_count > overall_best_count or (best_count == overall_best_count and best_weight > overall_best_weight):
                overall_best_count = best_count
                overall_best_weight = best_weight
                overall_best_assignment = best_assignment
        
        if overall_best_assignment is None:
            overall_best_assignment = {v['id']: [] for v in owned_vehicles}
        
        results = []
        total_cost = 0.0
        total_fuel_cost = 0.0
        assigned_cargo_ids = set()
        
        for vehicle in owned_vehicles:
            assigned_cargos = overall_best_assignment.get(vehicle['id'], [])
            if not assigned_cargos:
                continue
            
            for c in assigned_cargos:
                assigned_cargo_ids.add(c['id'])
            
            result = self._build_route_result(vehicle, assigned_cargos, dist_matrix, depot_id)
            if result:
                results.append(result)
                total_cost += result['cost']
                total_fuel_cost += result['fuel_cost']
        
        remaining_cargos = [c for c in self.cargos if c['id'] not in assigned_cargo_ids]
        undelivered_details = []
        for cargo in remaining_cargos:
            station_name = self.stations.get(cargo['station_id'], {}).get('name', 'Bilinmiyor')
            undelivered_details.append({
                'id': cargo['id'],
                'weight': cargo['weight'],
                'station_id': cargo['station_id'],
                'station_name': station_name
            })
        
        return {
            'routes': results,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_cargos': sum(r['cargo_count'] for r in results),
            'total_weight': round(sum(r['weight'] for r in results), 2),
            'undelivered': remaining_cargos,
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }
    
    def _find_best_vehicle_combination(self, cargos: List[Dict], vehicles: List[Dict], 
                                        dist_matrix: Dict, depot_id: Optional[int], mode: str) -> Optional[Dict]:
        total_weight = sum(c['weight'] for c in cargos)
        
        best_single = None
        best_single_cost = float('inf')
        
        for vehicle in vehicles:
            if vehicle['capacity'] >= total_weight:
                route, selected, distance, cost = self.greedy_route(cargos, vehicle['capacity'], vehicle)
                if len(selected) == len(cargos) and cost < best_single_cost:
                    best_single_cost = cost
                    best_single = self._build_route_result(vehicle, selected, dist_matrix, depot_id)
        
        if best_single:
            return {
                'routes': [best_single],
                'total_cost': round(best_single['cost'], 2),
                'total_fuel_cost': round(best_single['fuel_cost'], 2),
                'total_cargos': best_single['cargo_count'],
                'total_weight': round(best_single['weight'], 2),
                'undelivered': [],
                'undelivered_details': [],
                'optimize_for': self.optimize_for
            }
        
        return None
    
    def _heuristic_max_count_assignment(self, all_cargos: List[Dict], owned_vehicles: List[Dict]) -> Dict[int, List]:
        best_assignment = None
        best_count = -1
        
        orderings = [
            sorted(all_cargos, key=lambda c: c['weight']),
            sorted(all_cargos, key=lambda c: c['weight'], reverse=True),
            sorted(all_cargos, key=lambda c: c['station_id']),
        ]
        
        for cargos_ordered in orderings:
            assignment = {v['id']: [] for v in owned_vehicles}
            weights = {v['id']: 0.0 for v in owned_vehicles}
            
            for cargo in cargos_ordered:
                best_v = None
                best_rem = float('inf')
                
                for v in owned_vehicles:
                    rem = v['capacity'] - weights[v['id']]
                    if cargo['weight'] <= rem and rem < best_rem:
                        best_rem = rem
                        best_v = v
                
                if best_v:
                    assignment[best_v['id']].append(cargo)
                    weights[best_v['id']] += cargo['weight']
            
            count = sum(len(c) for c in assignment.values())
            if count > best_count:
                best_count = count
                best_assignment = assignment
        
        return best_assignment if best_assignment else {v['id']: [] for v in owned_vehicles}
    
    def _heuristic_max_weight_assignment(self, all_cargos: List[Dict], owned_vehicles: List[Dict]) -> Dict[int, List]:
        best_assignment = None
        best_weight = -1
        
        orderings = [
            sorted(all_cargos, key=lambda c: c['weight'], reverse=True),
            sorted(all_cargos, key=lambda c: c['weight']),
            sorted(all_cargos, key=lambda c: c['station_id']),
        ]
        
        for cargos_ordered in orderings:
            assignment = {v['id']: [] for v in owned_vehicles}
            weights = {v['id']: 0.0 for v in owned_vehicles}
            
            for cargo in cargos_ordered:
                best_v = None
                min_waste = float('inf')
                
                for v in owned_vehicles:
                    rem = v['capacity'] - weights[v['id']]
                    if cargo['weight'] <= rem:
                        waste = rem - cargo['weight']
                        if waste < min_waste:
                            min_waste = waste
                            best_v = v
                
                if best_v:
                    assignment[best_v['id']].append(cargo)
                    weights[best_v['id']] += cargo['weight']
            
            total_weight = sum(weights.values())
            if total_weight > best_weight:
                best_weight = total_weight
                best_assignment = assignment
        
        return best_assignment if best_assignment else {v['id']: [] for v in owned_vehicles}
    
    def _solve_max_count_global(self, dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        owned_vehicles = sorted([v for v in self.vehicles if v['is_owned']], key=lambda v: v['capacity'], reverse=True)
        all_cargos = list(self.cargos)
        
        if not all_cargos or not owned_vehicles:
            return {
                'routes': [],
                'total_cost': 0,
                'total_fuel_cost': 0,
                'total_cargos': 0,
                'total_weight': 0,
                'undelivered': all_cargos,
                'undelivered_details': [{'id': c['id'], 'weight': c['weight'], 'station_id': c['station_id'], 
                                         'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')} 
                                        for c in all_cargos],
                'optimize_for': self.optimize_for
            }
        
        vehicle_caps = {v['id']: v['capacity'] for v in owned_vehicles}
        
        orderings = [
            sorted(all_cargos, key=lambda c: c['weight'], reverse=True),
            sorted(all_cargos, key=lambda c: c['weight']),
            sorted(all_cargos, key=lambda c: (c['station_id'], -c['weight'])),
            all_cargos,
        ]
        
        overall_best_assignment = None
        overall_best_count = -1
        overall_best_weight = -1
        
        for cargo_order in orderings:
            best_assignment = None
            best_count = -1
            best_weight = -1
            
            def backtrack(cargo_idx: int, current_assignment: Dict[int, List], current_weights: Dict[int, float]):
                nonlocal best_assignment, best_count, best_weight
                
                if cargo_idx == len(cargo_order):
                    total_count = sum(len(cargos) for cargos in current_assignment.values())
                    total_wt = sum(current_weights.values())
                    
                    if total_count > best_count or (total_count == best_count and total_wt > best_weight):
                        best_count = total_count
                        best_weight = total_wt
                        best_assignment = {vid: list(cargos) for vid, cargos in current_assignment.items()}
                    return
                
                cargo = cargo_order[cargo_idx]
                cargo_weight = cargo['weight']
                
                remaining_cargos_count = len(cargo_order) - cargo_idx
                current_count = sum(len(cargos) for cargos in current_assignment.values())
                if current_count + remaining_cargos_count <= best_count:
                    return
                
                tried_capacities = set()
                for vehicle in owned_vehicles:
                    vid = vehicle['id']
                    remaining_cap = vehicle_caps[vid] - current_weights[vid]
                    
                    cap_key = round(remaining_cap, 2)
                    if cap_key in tried_capacities:
                        continue
                    
                    if cargo_weight <= remaining_cap:
                        tried_capacities.add(cap_key)
                        current_assignment[vid].append(cargo)
                        current_weights[vid] += cargo_weight
                        backtrack(cargo_idx + 1, current_assignment, current_weights)
                        current_assignment[vid].pop()
                        current_weights[vid] -= cargo_weight
                
                backtrack(cargo_idx + 1, current_assignment, current_weights)
            
            if len(cargo_order) > 18:
                assignment = self._heuristic_max_count_assignment(cargo_order, owned_vehicles)
                count = sum(len(c) for c in assignment.values())
                weight = sum(sum(cargo['weight'] for cargo in cargos) for cargos in assignment.values())
                if count > best_count or (count == best_count and weight > best_weight):
                    best_count = count
                    best_weight = weight
                    best_assignment = assignment
            else:
                initial_assignment = {v['id']: [] for v in owned_vehicles}
                initial_weights = {v['id']: 0.0 for v in owned_vehicles}
                backtrack(0, initial_assignment, initial_weights)
            
            if best_count > overall_best_count or (best_count == overall_best_count and best_weight > overall_best_weight):
                overall_best_count = best_count
                overall_best_weight = best_weight
                overall_best_assignment = best_assignment
        
        if overall_best_assignment is None:
            overall_best_assignment = {v['id']: [] for v in owned_vehicles}
        
        results = []
        total_cost = 0.0
        total_fuel_cost = 0.0
        assigned_cargo_ids = set()
        
        for vehicle in owned_vehicles:
            assigned_cargos = overall_best_assignment.get(vehicle['id'], [])
            if not assigned_cargos:
                continue
            
            for c in assigned_cargos:
                assigned_cargo_ids.add(c['id'])
            
            result = self._build_route_result(vehicle, assigned_cargos, dist_matrix, depot_id)
            if result:
                results.append(result)
                total_cost += result['cost']
                total_fuel_cost += result['fuel_cost']
        
        remaining_cargos = [c for c in self.cargos if c['id'] not in assigned_cargo_ids]
        undelivered_details = []
        for cargo in remaining_cargos:
            station_name = self.stations.get(cargo['station_id'], {}).get('name', 'Bilinmiyor')
            undelivered_details.append({
                'id': cargo['id'],
                'weight': cargo['weight'],
                'station_id': cargo['station_id'],
                'station_name': station_name
            })
        
        return {
            'routes': results,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_cargos': sum(r['cargo_count'] for r in results),
            'total_weight': round(sum(r['weight'] for r in results), 2),
            'undelivered': remaining_cargos,
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }
    
    def _solve_max_weight_global(self, dist_matrix: Dict, depot_id: Optional[int]) -> Dict:
        owned_vehicles = sorted([v for v in self.vehicles if v['is_owned']], key=lambda v: v['capacity'], reverse=True)
        all_cargos = list(self.cargos)
        
        if not all_cargos or not owned_vehicles:
            return {
                'routes': [],
                'total_cost': 0,
                'total_fuel_cost': 0,
                'total_cargos': 0,
                'total_weight': 0,
                'undelivered': all_cargos,
                'undelivered_details': [{'id': c['id'], 'weight': c['weight'], 'station_id': c['station_id'], 
                                         'station_name': self.stations.get(c['station_id'], {}).get('name', 'Bilinmiyor')} 
                                        for c in all_cargos],
                'optimize_for': self.optimize_for
            }
        
        vehicle_caps = {v['id']: v['capacity'] for v in owned_vehicles}
        total_capacity = sum(vehicle_caps.values())
        
        orderings = [
            sorted(all_cargos, key=lambda c: c['weight'], reverse=True),
            sorted(all_cargos, key=lambda c: c['weight']),
            sorted(all_cargos, key=lambda c: (c['station_id'], -c['weight'])),
            all_cargos,
        ]
        
        overall_best_assignment = None
        overall_best_weight = -1
        overall_best_count = -1
        
        for cargo_order in orderings:
            best_assignment = None
            best_weight = -1
            best_count = -1
            
            def backtrack(cargo_idx: int, current_assignment: Dict[int, List], current_weights: Dict[int, float]):
                nonlocal best_assignment, best_weight, best_count
                
                if cargo_idx == len(cargo_order):
                    total_wt = sum(current_weights.values())
                    total_cnt = sum(len(cargos) for cargos in current_assignment.values())
                    
                    if total_wt > best_weight or (total_wt == best_weight and total_cnt > best_count):
                        best_weight = total_wt
                        best_count = total_cnt
                        best_assignment = {vid: list(cargos) for vid, cargos in current_assignment.items()}
                    return
                
                cargo = cargo_order[cargo_idx]
                cargo_weight = cargo['weight']
                
                current_total_weight = sum(current_weights.values())
                remaining_capacity = total_capacity - current_total_weight
                remaining_cargo_weight = sum(c['weight'] for c in cargo_order[cargo_idx:])
                max_potential = current_total_weight + min(remaining_capacity, remaining_cargo_weight)
                
                if max_potential <= best_weight:
                    return
                
                tried_capacities = set()
                for vehicle in owned_vehicles:
                    vid = vehicle['id']
                    remaining_cap = vehicle_caps[vid] - current_weights[vid]
                    cap_key = round(remaining_cap, 2)
                    if cap_key in tried_capacities:
                        continue
                    
                    if cargo_weight <= remaining_cap:
                        tried_capacities.add(cap_key)
                        current_assignment[vid].append(cargo)
                        current_weights[vid] += cargo_weight
                        backtrack(cargo_idx + 1, current_assignment, current_weights)
                        current_assignment[vid].pop()
                        current_weights[vid] -= cargo_weight
                
                backtrack(cargo_idx + 1, current_assignment, current_weights)
            
            if len(cargo_order) > 18:
                assignment = self._heuristic_max_weight_assignment(cargo_order, owned_vehicles)
                weight = sum(sum(c['weight'] for c in cargos) for cargos in assignment.values())
                count = sum(len(c) for c in assignment.values())
                if weight > best_weight or (weight == best_weight and count > best_count):
                    best_weight = weight
                    best_count = count
                    best_assignment = assignment
            else:
                initial_assignment = {v['id']: [] for v in owned_vehicles}
                initial_weights = {v['id']: 0.0 for v in owned_vehicles}
                backtrack(0, initial_assignment, initial_weights)
            
            if best_weight > overall_best_weight or (best_weight == overall_best_weight and best_count > overall_best_count):
                overall_best_weight = best_weight
                overall_best_count = best_count
                overall_best_assignment = best_assignment
        
        if overall_best_assignment is None:
            overall_best_assignment = {v['id']: [] for v in owned_vehicles}
        
        results = []
        total_cost = 0.0
        total_fuel_cost = 0.0
        assigned_cargo_ids = set()
        
        for vehicle in owned_vehicles:
            assigned_cargos = overall_best_assignment.get(vehicle['id'], [])
            if not assigned_cargos:
                continue
            
            for c in assigned_cargos:
                assigned_cargo_ids.add(c['id'])
            
            result = self._build_route_result(vehicle, assigned_cargos, dist_matrix, depot_id)
            if result:
                results.append(result)
                total_cost += result['cost']
                total_fuel_cost += result['fuel_cost']
        
        remaining_cargos = [c for c in self.cargos if c['id'] not in assigned_cargo_ids]
        undelivered_details = []
        for cargo in remaining_cargos:
            station_name = self.stations.get(cargo['station_id'], {}).get('name', 'Bilinmiyor')
            undelivered_details.append({
                'id': cargo['id'],
                'weight': cargo['weight'],
                'station_id': cargo['station_id'],
                'station_name': station_name
            })
        
        return {
            'routes': results,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_cargos': sum(r['cargo_count'] for r in results),
            'total_weight': round(sum(r['weight'] for r in results), 2),
            'undelivered': remaining_cargos,
            'undelivered_details': undelivered_details,
            'optimize_for': self.optimize_for
        }
    
    def solve_unlimited_vehicles(self) -> Dict:
        limited_result = self.solve_limited_vehicles()
        
        remaining_cargos = limited_result.get('undelivered', [])
        if not remaining_cargos or len(remaining_cargos) == 0:
            return limited_result
        
        results = list(limited_result['routes'])
        total_cost = limited_result['total_cost']
        total_fuel_cost = limited_result.get('total_fuel_cost', 0)
        rented_count = 0
        
        while remaining_cargos:
            rented_vehicle = {
                'id': f'rented_{rented_count + 1}',
                'name': f'Kiralık Araç {rented_count + 1}',
                'capacity': self.params['rental_capacity'],
                'rental_cost': self.params['rental_cost'],
                'fuel_consumption': 0.1,
                'is_owned': False
            }
            
            route, selected, distance, route_cost = self.greedy_route(remaining_cargos, rented_vehicle['capacity'], rented_vehicle)
            
            if not selected:
                break
            
            road_cost = distance * self.params['cost_per_km']
            cost = self.params['rental_cost'] + road_cost
            total_weight = sum(c['weight'] for c in selected)
            
            cargo_users = []
            for c in selected:
                if c.get('user_id'):
                    cargo_users.append({'cargo_id': c['id'], 'user_id': c['user_id'], 'username': c.get('username', 'Bilinmiyor'), 'weight': c['weight'], 'station': c.get('station_name', '')})
            
            results.append({
                'vehicle': rented_vehicle,
                'route': route,
                'route_names': [self.stations[sid]['name'] for sid in route if sid in self.stations],
                'cargos': selected,
                'cargo_users': cargo_users,
                'distance': round(distance, 2),
                'fuel_cost': round(road_cost, 2),
                'cost': round(cost, 2),
                'weight': total_weight,
                'cargo_count': len(selected),
                'is_rented': True
            })
            
            total_cost += cost
            total_fuel_cost += road_cost
            rented_count += 1
            selected_ids = {c['id'] for c in selected}
            remaining_cargos = [c for c in remaining_cargos if c['id'] not in selected_ids]
        
        return {
            'routes': results,
            'total_cost': round(total_cost, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_cargos': sum(r['cargo_count'] for r in results),
            'total_weight': sum(r['weight'] for r in results),
            'rented_vehicles': rented_count,
            'rental_cost': rented_count * self.params['rental_cost'],
            'optimize_for': self.optimize_for,
            'undelivered': [],
            'undelivered_count': 0,
            'undelivered_details': []
        }

class KargoHandler(SimpleHTTPRequestHandler):
    pass
    
    def __init__(self, *args, **kwargs):
        self.static_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=self.static_dir, **kwargs)
    
    def send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Cookie')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_session(self) -> Optional[Dict]:
        cookie = self.headers.get('Cookie', '')
        for part in cookie.split(';'):
            if 'session_id=' in part:
                session_id = part.split('=')[1].strip()
                return sessions.get(session_id)
        return None
    
    def set_session(self, user_data: Dict) -> str:
        session_id = str(uuid.uuid4())
        sessions[session_id] = user_data
        return session_id
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Cookie')
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/session':
            self.handle_session()
        elif path == '/api/stations':
            self.handle_get_stations()
        elif path == '/api/vehicles':
            self.handle_get_vehicles()
        elif path == '/api/cargos':
            self.handle_get_cargos()
        elif path == '/api/routes':
            self.handle_get_routes()
        elif path == '/api/my-route':
            self.handle_get_my_route()
        elif path == '/api/parameters':
            self.handle_get_parameters()
        elif path == '/api/stats':
            self.handle_get_stats()
        elif path == '/api/users':
            self.handle_get_users()
        elif path == '/api/reset-codes':
            self.handle_get_reset_codes()
        elif path == '/api/db-stats':
            self.handle_get_db_stats()
        elif path == '/api/db-data':
            self.handle_get_db_data()
        elif path == '/db-view' or path == '/database' or path == '/db-view.html':
            self.serve_db_view()
        elif path == '/' or path == '/index.html':
            self.serve_html()
        elif path.startswith('/static/'):
            self.serve_static(path)
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        
        if path == '/api/login':
            self.handle_login(data)
        elif path == '/api/logout':
            self.handle_logout()
        elif path == '/api/register':
            self.handle_register(data)
        elif path == '/api/forgot-password':
            self.handle_forgot_password(data)
        elif path == '/api/reset-password':
            self.handle_reset_password(data)
        elif path == '/api/stations':
            self.handle_add_station(data)
        elif path == '/api/vehicles':
            self.handle_add_vehicle(data)
        elif path == '/api/cargos':
            self.handle_add_cargo(data)
        elif path == '/api/load-scenario':
            self.handle_load_scenario(data)
        elif path == '/api/optimize':
            self.handle_optimize(data)
        elif path == '/api/compare-scenarios':
            self.handle_compare_scenarios(data)
        elif path == '/api/compare-pending':
            self.handle_compare_pending(data)
        elif path == '/api/route-geometry':
            self.handle_route_geometry(data)
        else:
            self.send_json({'error': 'Not Found'}, 404)
    
    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        data = json.loads(body) if body else {}
        
        if path == '/api/parameters':
            self.handle_update_parameters(data)
        else:
            self.send_json({'error': 'Not Found'}, 404)
    
    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path.startswith('/api/stations/'):
            station_id = int(path.split('/')[-1])
            self.handle_delete_station(station_id)
        elif path.startswith('/api/users/'):
            user_id = int(path.split('/')[-1])
            self.handle_delete_user(user_id)
        elif path.startswith('/api/cargos/'):
            cargo_id = int(path.split('/')[-1])
            self.handle_delete_cargo(cargo_id)
        elif path.startswith('/api/vehicles/'):
            vehicle_id = int(path.split('/')[-1])
            self.handle_delete_vehicle(vehicle_id)
        elif path.startswith('/api/routes/'):
            route_id = int(path.split('/')[-1])
            self.handle_delete_route(route_id)
        else:
            self.send_json({'error': 'Not Found'}, 404)
    
    def serve_html(self):
        html_path = os.path.join(self.static_dir, 'templates', 'index.html')
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
    
    def serve_db_view(self):
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'db-view.html')
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            # Fallback HTML
            html = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Veritabanı Görüntüleyici - Kargo Sistemi</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        h1 { color: #333; }
        h2 { color: #3498db; margin-top: 30px; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; background: white; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #3498db; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        a { color: #3498db; text-decoration: none; }
        .badge { padding: 3px 8px; border-radius: 10px; font-size: 12px; }
        .admin { background: #e74c3c; color: white; }
        .user { background: #27ae60; color: white; }
    </style>
</head>
<body>
    <a href="/">← Ana Sayfa</a>
    <h1>Veritabanı Görüntüleyici</h1>
    <div id="content">Yükleniyor...</div>
    <script>
        fetch('/api/db-data')
            .then(r => r.json())
            .then(data => {
                if (!data.success) {
                    document.getElementById('content').innerHTML = 'Hata: ' + data.error;
                    return;
                }
                let h = '<h2>Kullanıcılar</h2><table><tr><th>ID</th><th>Kullanıcı</th><th>Şifre</th><th>Rol</th><th>Tarih</th></tr>';
                data.users.forEach(u => {
                    let passDisplay = u.plain_password || '<span style="color:#e74c3c">Bilinmiyor (eski kayıt)</span>';
                    h += '<tr><td>'+u.id+'</td><td>'+u.username+'</td><td><strong style="color:#27ae60">'+passDisplay+'</strong></td><td><span class="badge '+u.role+'">'+u.role+'</span></td><td>'+u.created_at+'</td></tr>';
                });
                h += '</table>';
                
                h += '<h2>İstasyonlar</h2><table><tr><th>ID</th><th>Ad</th><th>Enlem</th><th>Boylam</th></tr>';
                data.stations.forEach(s => {
                    h += '<tr><td>'+s.id+'</td><td>'+s.name+'</td><td>'+s.latitude+'</td><td>'+s.longitude+'</td></tr>';
                });
                h += '</table>';
                
                h += '<h2>Araçlar</h2><table><tr><th>ID</th><th>Ad</th><th>Kapasite</th><th>Sahiplik</th></tr>';
                data.vehicles.forEach(v => {
                    h += '<tr><td>'+v.id+'</td><td>'+v.name+'</td><td>'+v.capacity+'</td><td>'+(v.is_owned ? 'Sahip' : 'Kiralı')+'</td></tr>';
                });
                h += '</table>';
                
                h += '<h2>Kargolar (Son 50)</h2><table><tr><th>ID</th><th>Kullanıcı</th><th>İstasyon</th><th>Ağırlık</th><th>Durum</th></tr>';
                data.cargos.forEach(c => {
                    h += '<tr><td>'+c.id+'</td><td>'+(c.username || c.user_id)+'</td><td>'+(c.station_name || c.station_id)+'</td><td>'+c.weight+'kg</td><td>'+c.status+'</td></tr>';
                });
                h += '</table>';
                
                document.getElementById('content').innerHTML = h;
            })
            .catch(e => {
                document.getElementById('content').innerHTML = 'Hata: ' + e.message;
            });
    </script>
</body>
</html>'''
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
    
    def handle_get_db_data(self):
        conn = get_db()
        if not conn:
            self.send_json({'success': False, 'error': 'Veritabani baglantisi kurulamadi'})
            return
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, password, plain_password, role, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at FROM users ORDER BY id")
            users = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT id, name, latitude, longitude, is_active FROM stations ORDER BY id")
            stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT id, name, capacity, is_owned FROM vehicles ORDER BY id")
            vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT c.id, c.user_id, c.station_id, c.weight, c.status, s.name as station_name, DATE_FORMAT(c.created_at, '%Y-%m-%d %H:%i:%s') as created_at FROM cargos c LEFT JOIN stations s ON c.station_id = s.id ORDER BY c.id DESC LIMIT 50")
            cargos = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT id, vehicle_id, total_distance, total_cost, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at FROM routes ORDER BY id DESC LIMIT 20")
            routes = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            self.send_json({
                'success': True,
                'users': users,
                'stations': stations,
                'vehicles': vehicles,
                'cargos': cargos,
                'routes': routes
            })
        except Exception as e:
            print(f"DB Data Hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'success': False, 'error': str(e)})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def serve_static(self, path: str):
        file_path = os.path.join(self.static_dir, path.lstrip('/'))
        try:
            if path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp')):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                content_type = 'image/png'
                if path.endswith('.jpg') or path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif path.endswith('.gif'):
                    content_type = 'image/gif'
                elif path.endswith('.ico'):
                    content_type = 'image/x-icon'
                elif path.endswith('.webp'):
                    content_type = 'image/webp'
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_type = 'text/plain'
                if path.endswith('.css'):
                    content_type = 'text/css'
                elif path.endswith('.js'):
                    content_type = 'application/javascript'
                
                self.send_response(200)
                self.send_header('Content-Type', f'{content_type}; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
    
    def handle_session(self):
        session = self.get_session()
        if session:
            self.send_json({'logged_in': True, 'user_id': session['user_id'], 'username': session['username'], 'role': session['role']})
        else:
            self.send_json({'logged_in': False})
    
    def handle_login(self, data: Dict):
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            password = hashlib.sha256(data.get('password', '').encode()).hexdigest()
            cursor.execute("SELECT id, username, role FROM users WHERE username=%s AND password=%s", (data.get('username'), password))
            user = cursor.fetchone()
            
            if user:
                user_id, username, role = user
                session_id = self.set_session({'user_id': user_id, 'username': username, 'role': role})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Set-Cookie', f'session_id={session_id}; Path=/')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'role': role, 'username': username}, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_json({'error': 'Geçersiz kullanıcı adı veya şifre'}, 401)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def handle_logout(self):
        cookie = self.headers.get('Cookie', '')
        for part in cookie.split(';'):
            if 'session_id=' in part:
                session_id = part.split('=')[1].strip()
                if session_id in sessions:
                    del sessions[session_id]
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Set-Cookie', 'session_id=; Path=/; Max-Age=0')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
    
    def handle_register(self, data: Dict):
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            self.send_json({'error': 'Tüm alanları doldurun'}, 400)
            return
        
        try:
            cursor = conn.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, email, password, plain_password, role) VALUES (%s, %s, %s, %s, 'user')", 
                          (username, email, password_hash, password))
            conn.commit()
            cursor.close()
            conn.close()
            self.send_json({'success': True})
        except mysql.connector.IntegrityError as e:
            conn.close()
            if 'email' in str(e).lower():
                self.send_json({'error': 'Bu e-posta adresi zaten kayıtlı'}, 400)
            else:
                self.send_json({'error': 'Bu kullanıcı adı zaten mevcut'}, 400)

    def handle_forgot_password(self, data: Dict):
        """Şifremi unuttum - e-posta ile kod gönder"""
        email = data.get('email', '').strip()
        
        if not email:
            self.send_json({'error': 'E-posta adresi gerekli'}, 400)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                self.send_json({'error': 'Bu e-posta adresi kayıtlı değil'}, 404)
                return
            
            user_id: int = int(user['id'])  # type: ignore
            username: str = str(user['username'])  # type: ignore
            
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            expires_at = datetime.now() + timedelta(minutes=15)
            
            cursor.execute("DELETE FROM password_reset_codes WHERE user_id = %s", (user_id,))
            cursor.execute(
                "INSERT INTO password_reset_codes (user_id, code, expires_at) VALUES (%s, %s, %s)",
                (user_id, code, expires_at)
            )
            conn.commit()
            
            email_sent = self.send_reset_email(email, username, code)
            
            cursor.close()
            conn.close()
            
            if email_sent:
                self.send_json({'success': True, 'message': 'Doğrulama kodu e-posta adresinize gönderildi'})
            else:
                self.send_json({'success': True, 'message': f'Doğrulama kodunuz: {code} (E-posta gönderilemedi)', 'code': code})
        except Exception as e:
            conn.close()
            self.send_json({'error': f'Bir hata oluştu: {str(e)}'}, 500)

    def handle_reset_password(self, data: Dict):
        """Şifre sıfırlama - kod ile yeni şifre belirleme"""
        email = data.get('email', '').strip()
        code = data.get('code', '').strip()
        new_password = data.get('new_password', '')
        
        if not email or not code or not new_password:
            self.send_json({'error': 'Tüm alanları doldurun'}, 400)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                self.send_json({'error': 'Geçersiz e-posta adresi'}, 400)
                return
            
            user_id: int = int(user['id'])  # type: ignore
            
            cursor.execute("""
                SELECT id FROM password_reset_codes 
                WHERE user_id = %s AND code = %s AND used = 0 AND expires_at > NOW()
            """, (user_id, code))
            reset_code = cursor.fetchone()
            
            if not reset_code:
                cursor.close()
                conn.close()
                self.send_json({'error': 'Geçersiz veya süresi dolmuş kod'}, 400)
                return
            
            reset_code_id: int = int(reset_code['id'])  # type: ignore
            
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (password_hash, user_id))
            cursor.execute("UPDATE password_reset_codes SET used = 1 WHERE id = %s", (reset_code_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json({'success': True, 'message': 'Şifreniz başarıyla değiştirildi'})
        except Exception as e:
            conn.close()
            self.send_json({'error': f'Bir hata oluştu: {str(e)}'}, 500)

    def handle_get_stations(self):
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, latitude, longitude, is_active FROM stations WHERE is_active=1")
        stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        self.send_json(stations)

    def handle_add_station(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO stations (name, latitude, longitude) VALUES (%s, %s, %s)", (data['name'], data['latitude'], data['longitude']))
            conn.commit()
            cursor.close()
            conn.close()
            self.send_json({'success': True})
        except mysql.connector.IntegrityError:
            conn.close()
            self.send_json({'error': 'Bu istasyon zaten mevcut'}, 400)

    def handle_delete_station(self, station_id: int):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("UPDATE stations SET is_active=0 WHERE id=%s", (station_id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_get_vehicles(self):
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        self.send_json(vehicles)

    def handle_add_vehicle(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (name, capacity, rental_cost, fuel_consumption, is_owned) VALUES (%s, %s, %s, %s, %s)",
            (data['name'], data['capacity'], data.get('rental_cost', 0), data.get('fuel_consumption', 0.1), data.get('is_owned', 1)))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_delete_vehicle(self, vehicle_id: int):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_delete_route(self, route_id: int):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM routes WHERE id=%s", (route_id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_get_cargos(self):
        session = self.get_session()
        if not session:
            self.send_json({'error': 'Giriş yapmanız gerekiyor'}, 401)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        
        if session['role'] == 'admin':
            cursor.execute("""
                SELECT c.id, c.user_id, c.station_id, c.weight, c.status, c.delivery_date, c.created_at,
                       s.name as station_name, u.username 
                FROM cargos c 
                JOIN stations s ON c.station_id = s.id 
                LEFT JOIN users u ON c.user_id = u.id
                ORDER BY c.created_at DESC
            """)
        else:
            cursor.execute("""
                SELECT c.id, c.user_id, c.station_id, c.weight, c.status, c.delivery_date, c.created_at,
                       s.name as station_name, NULL as username
                FROM cargos c 
                JOIN stations s ON c.station_id = s.id 
                WHERE c.user_id = %s
                ORDER BY c.created_at DESC
            """, (session['user_id'],))
        
        cargos = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        
        for cargo in cargos:
            if cargo.get('created_at'):
                cargo['created_at'] = str(cargo['created_at'])
            if cargo.get('delivery_date'):
                cargo['delivery_date'] = str(cargo['delivery_date'])
        
        cursor.close()
        conn.close()
        self.send_json(cargos)

    def handle_add_cargo(self, data: Dict):
        session = self.get_session()
        if not session:
            self.send_json({'error': 'Giriş yapmanız gerekiyor'}, 401)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM stations WHERE id=%s AND is_active=1", (data['station_id'],))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            self.send_json({'error': 'Geçersiz istasyon'}, 400)
            return
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        delivery_date = data.get('delivery_date') or tomorrow
        cursor.execute("INSERT INTO cargos (user_id, station_id, weight, delivery_date) VALUES (%s, %s, %s, %s)",
            (session['user_id'], data['station_id'], data['weight'], delivery_date))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_delete_cargo(self, cargo_id: int):
        session = self.get_session()
        if not session:
            self.send_json({'error': 'Giriş yapmanız gerekiyor'}, 401)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        if session['role'] == 'admin':
            cursor.execute("DELETE FROM cargos WHERE id=%s", (cargo_id,))
        else:
            cursor.execute("DELETE FROM cargos WHERE id=%s AND user_id=%s", (cargo_id, session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()
        self.send_json({'success': True})

    def handle_load_scenario(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        scenario = data.get('scenario', [])
        scenario_num = data.get('scenario_num', 1)
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM route_cargos")
            cursor.execute("DELETE FROM routes")
            cursor.execute("DELETE FROM cargos WHERE status = 'pending'")
            
            cargo_count = 0
            delivery_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            for item in scenario:
                cursor.execute("SELECT id FROM stations WHERE name LIKE %s", (f"%{item['district']}%",))
                row = cursor.fetchone()
                if row and item['count'] > 0:
                    station_id = int(str(row[0]))
                    avg_weight = item['weight'] / item['count'] if item['count'] > 0 else 0
                    for _ in range(int(item['count'])):
                        cursor.execute(
                            "INSERT INTO cargos (station_id, weight, status, delivery_date) VALUES (%s, %s, 'pending', %s)", 
                            (station_id, float(avg_weight), delivery_date)
                        )
                        cargo_count += 1
            
            self.send_json({'success': True, 'cargo_count': cargo_count, 'scenario': scenario_num})
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_optimize(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        problem_type = data.get('type', 'limited')
        optimize_for = data.get('optimize_for', 'balanced')
        delivery_date = data.get('delivery_date', None)
        cargo_ids = data.get('cargo_ids', [])
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Eğer cargo_ids verilmişse, sadece o cargo'ları kullan
            if cargo_ids:
                placeholders = ','.join(['%s'] * len(cargo_ids))
                cursor.execute(f"""
                    SELECT c.id, c.user_id, c.station_id, c.weight, c.status,
                           s.name as station_name, s.latitude, s.longitude,
                           u.username
                    FROM cargos c 
                    JOIN stations s ON c.station_id = s.id 
                    LEFT JOIN users u ON c.user_id = u.id
                    WHERE c.status = 'pending' AND c.id IN ({placeholders})
                """, cargo_ids)
            elif delivery_date:
                cursor.execute("""
                    SELECT c.id, c.user_id, c.station_id, c.weight, c.status,
                           s.name as station_name, s.latitude, s.longitude,
                           u.username
                    FROM cargos c 
                    JOIN stations s ON c.station_id = s.id 
                    LEFT JOIN users u ON c.user_id = u.id
                    WHERE c.status = 'pending' AND c.delivery_date = %s
                """, (delivery_date,))
            else:
                cursor.execute("""
                    SELECT c.id, c.user_id, c.station_id, c.weight, c.status,
                           s.name as station_name, s.latitude, s.longitude,
                           u.username
                    FROM cargos c 
                    JOIN stations s ON c.station_id = s.id 
                    LEFT JOIN users u ON c.user_id = u.id
                    WHERE c.status = 'pending'
                """)
            cargos = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM stations WHERE is_active=1")
            stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM vehicles WHERE is_owned=1")
            vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM parameters WHERE id=1")
            params_row = cursor.fetchone()
            params = dict_from_row(cursor, params_row) if params_row else {'cost_per_km': 1.0, 'rental_cost': 200, 'rental_capacity': 500}
            
            if not cargos:
                self.send_json({'error': 'Bekleyen kargo yok'}, 400)
                return
            
            optimizer = RouteOptimizer(stations, cargos, vehicles, params, optimize_for)
            
            if problem_type == 'unlimited':
                result = optimizer.solve_unlimited_vehicles()
            else:
                result = optimizer.solve_limited_vehicles()
            
            for route_data in result['routes']:
                vehicle_id = route_data['vehicle'].get('id') if isinstance(route_data['vehicle'].get('id'), int) else None
                cursor.execute("INSERT INTO routes (vehicle_id, route_data, total_distance, total_cost, total_weight, cargo_count) VALUES (%s, %s, %s, %s, %s, %s)",
                    (vehicle_id, json.dumps(route_data['route_names'], ensure_ascii=False), route_data['distance'], route_data['cost'], route_data['weight'], route_data['cargo_count']))
                route_id = cursor.lastrowid
                
                for cargo in route_data['cargos']:
                    cursor.execute("UPDATE cargos SET status='assigned' WHERE id=%s", (cargo['id'],))
                    cursor.execute("INSERT INTO route_cargos (route_id, cargo_id) VALUES (%s, %s)", (route_id, cargo['id']))
            
            conn.commit()
            self.send_json(result)
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Optimizasyon hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': f'Optimizasyon hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_route_geometry(self, data: Dict):
        route_stations = data.get('stations', [])
        
        if len(route_stations) < 2:
            self.send_json({'error': 'En az 2 istasyon gerekli'}, 400)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            coordinates = []
            for name in route_stations:
                cursor.execute("SELECT latitude, longitude FROM stations WHERE name=%s", (name,))
                station = cursor.fetchone()
                if station:
                    lat, lng = station
                    coordinates.append((lat, lng))
            
            if len(coordinates) < 2:
                self.send_json({'error': 'İstasyonlar bulunamadı'}, 400)
                return
            
            result = get_route_geometry(coordinates)
            if result:
                self.send_json(result)
            else:
                self.send_json({'error': 'Rota hesaplanamadı'}, 500)
        except Exception as e:
            print(f"Rota geometri hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': f'Rota hesaplama hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_get_routes(self):
        session = self.get_session()
        if not session:
            self.send_json({'error': 'Giriş yapmanız gerekiyor'}, 401)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            if session['role'] == 'admin':
                cursor.execute("""
                    SELECT r.*, v.name as vehicle_name 
                    FROM routes r 
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    ORDER BY r.created_at DESC
                """)
            else:
                cursor.execute("""
                    SELECT DISTINCT r.*, v.name as vehicle_name 
                    FROM routes r 
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    JOIN route_cargos rc ON r.id = rc.route_id
                    JOIN cargos c ON rc.cargo_id = c.id
                    WHERE c.user_id = %s
                    ORDER BY r.created_at DESC
                """, (session['user_id'],))
            
            routes = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            for route in routes:
                if route.get('created_at'):
                    route['created_at'] = str(route['created_at'])
            
            self.send_json(routes)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_get_parameters(self):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parameters WHERE id=1")
            row = cursor.fetchone()
            params = dict_from_row(cursor, row) if row else {
                'id': 1,
                'cost_per_km': 1.0,
                'rental_cost': 200,
                'rental_capacity': 500
            }
            self.send_json(params)
        except Exception as e:
            print(f"Parametreler hatası: {e}")
            self.send_json({'error': f'Veritabanı hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_update_parameters(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE parameters SET cost_per_km=%s, rental_cost=%s, rental_capacity=%s WHERE id=1",
                (data['cost_per_km'], data['rental_cost'], data['rental_capacity']))
            conn.commit()
            self.send_json({'success': True})
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Parametre güncelleme hatası: {e}")
            self.send_json({'error': f'Güncelleme hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_get_stats(self):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM cargos")
            result = cursor.fetchone()
            total_cargos = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM cargos WHERE status='pending'")
            result = cursor.fetchone()
            pending_cargos = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM routes")
            result = cursor.fetchone()
            total_routes = int(result[0]) if result else 0
            
            cursor.execute("SELECT COALESCE(SUM(total_distance), 0) FROM routes")
            result = cursor.fetchone()
            total_distance = float(result[0]) if result and result[0] else 0.0
            
            cursor.execute("SELECT COALESCE(SUM(total_cost), 0) FROM routes")
            result = cursor.fetchone()
            total_cost = float(result[0]) if result and result[0] else 0.0
            
            cursor.execute("SELECT COALESCE(SUM(weight), 0) FROM cargos WHERE status='assigned'")
            result = cursor.fetchone()
            total_weight = float(result[0]) if result and result[0] else 0.0
            
            cursor.execute("SELECT COUNT(*) FROM stations WHERE is_active=1")
            result = cursor.fetchone()
            stations_count = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            result = cursor.fetchone()
            vehicles_count = int(result[0]) if result else 0
            
            cursor.execute("""
                SELECT s.name, COUNT(c.id) as cargo_count, COALESCE(SUM(c.weight), 0) as total_weight
                FROM stations s
                LEFT JOIN cargos c ON s.id = c.station_id
                WHERE s.is_active = 1
                GROUP BY s.id, s.name
            """)
            station_distribution = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            self.send_json({
                'total_cargos': total_cargos,
                'pending_cargos': pending_cargos,
                'total_routes': total_routes,
                'total_distance': total_distance,
                'total_cost': total_cost,
                'total_weight': total_weight,
                'stations_count': stations_count,
                'vehicles_count': vehicles_count,
                'station_distribution': station_distribution
            })
        except Exception as e:
            print(f"Stats hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': f'Veritabanı hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_get_db_stats(self):
        """Veritabanı istatistikleri (Admin only)"""
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            result = cursor.fetchone()
            total_users = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
            result = cursor.fetchone()
            total_admins = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM stations WHERE is_active=1")
            result = cursor.fetchone()
            total_stations = int(result[0]) if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM cargos")
            result = cursor.fetchone()
            total_cargos = int(result[0]) if result else 0
            
            self.send_json({
                'total_users': total_users,
                'total_admins': total_admins,
                'total_stations': total_stations,
                'total_cargos': total_cargos
            })
        except Exception as e:
            print(f"DB stats hatası: {e}")
            self.send_json({'error': f'Veritabanı hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_delete_user(self, user_id: int):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        if session.get('user_id') == user_id:
            self.send_json({'error': 'Kendinizi silemezsiniz'}, 400)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            self.send_json({'success': True})
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Kullanıcı silme hatası: {e}")
            self.send_json({'error': f'Silme hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_compare_scenarios(self, data: Dict):
        """4 test senaryosu uzerinde 3 farkli optimizasyon modunu karsilastir"""
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        scenarios_data = data.get('scenarios', [])
        problem_type = data.get('type', 'limited')
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM stations WHERE is_active=1")
            stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM vehicles WHERE is_owned=1")
            vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM parameters WHERE id=1")
            params_row = cursor.fetchone()
            params = dict_from_row(cursor, params_row) if params_row else {'cost_per_km': 1.0, 'rental_cost': 200, 'rental_capacity': 500}
            
            cursor.close()
            
            results = []
            
            for scenario_num, scenario in enumerate(scenarios_data, 1):
                cargos = []
                cargo_id = 1
                for item in scenario:
                    station = next((s for s in stations if item['district'] in s['name']), None)
                    if station and item['count'] > 0:
                        avg_weight = item['weight'] / item['count']
                        for _ in range(item['count']):
                            cargos.append({
                                'id': cargo_id,
                                'station_id': station['id'],
                                'weight': avg_weight,
                                'station_name': station['name']
                            })
                            cargo_id += 1
                
                if cargos:
                    for opt_mode in ['balanced', 'max_count', 'max_weight']:
                        try:
                            optimizer = RouteOptimizer(stations, cargos, vehicles, params, opt_mode)
                            
                            if problem_type == 'unlimited':
                                result = optimizer.solve_unlimited_vehicles()
                            else:
                                result = optimizer.solve_limited_vehicles()
                            
                            undelivered_reason = ''
                            undelivered = result.get('undelivered', [])
                            if undelivered:
                                total_vehicle_capacity = sum(v['capacity'] for v in vehicles)
                                total_cargo_weight = sum(c['weight'] for c in cargos)
                                if problem_type == 'limited' and total_cargo_weight > total_vehicle_capacity:
                                    undelivered_reason = f'Kapasite yetersiz ({total_vehicle_capacity}kg < {total_cargo_weight}kg)'
                                else:
                                    max_vehicle_cap = max(v['capacity'] for v in vehicles) if vehicles else 0
                                    heavy = [c for c in undelivered if c['weight'] > max_vehicle_cap]
                                    if heavy:
                                        undelivered_reason = f'Kargo cok agir (max: {max_vehicle_cap}kg)'
                                    else:
                                        undelivered_reason = 'Arac kapasitesi yetersiz'
                            
                            results.append({
                                'scenario': scenario_num,
                                'problem_type': problem_type,
                                'optimize_for': opt_mode,
                                'total_cost': round(result['total_cost'], 2),
                                'total_fuel_cost': round(result.get('total_fuel_cost', 0), 2),
                                'total_cargos': result['total_cargos'],
                                'total_weight': result['total_weight'],
                                'vehicle_count': len(result['routes']),
                                'rented_vehicles': result.get('rented_vehicles', 0),
                                'undelivered_count': len(undelivered),
                                'undelivered_reason': undelivered_reason,
                                'undelivered_details': result.get('undelivered_details', []),
                                'routes': [
                                    {
                                        'vehicle_name': r['vehicle']['name'],
                                        'route_names': r.get('route_names', r.get('route', [])),
                                        'distance': r.get('distance', 0),
                                        'cost': r.get('cost', 0),
                                        'weight': r.get('weight', 0),
                                        'cargo_count': r.get('cargo_count', 0),
                                        'station_cargo_details': r.get('station_cargo_details', [])
                                    } for r in result.get('routes', [])
                                ]
                            })
                        except Exception as opt_error:
                            print(f"Optimizasyon hatası (scenario {scenario_num}, mode {opt_mode}): {opt_error}")
                            import traceback
                            traceback.print_exc()
                            results.append({
                                'scenario': scenario_num,
                                'problem_type': problem_type,
                                'optimize_for': opt_mode,
                                'error': str(opt_error),
                                'total_cost': 0,
                                'total_cargos': 0,
                                'total_weight': 0,
                                'vehicle_count': 0,
                                'undelivered_count': len(cargos)
                            })
            
            self.send_json({'success': True, 'comparison': results})
        except Exception as e:
            print(f"Senaryo Karşılaştırma Hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': str(e)}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    

    
    def send_reset_email(self, to_email: str, username: str, code: str) -> bool:
        try:
            smtp_server = EMAIL_CONFIG['smtp_server']
            smtp_port = EMAIL_CONFIG['smtp_port']
            sender_email = EMAIL_CONFIG['sender_email']
            sender_password = EMAIL_CONFIG['sender_password']
            sender_name = EMAIL_CONFIG['sender_name']

            msg = MIMEMultipart('alternative')
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = 'Kargo Sistemi - Şifre Sıfırlama Kodu'

            text_body = f"""
Merhaba {username},

Şifre sıfırlama talebiniz alındı.

Doğrulama Kodunuz: {code}

Bu kod 15 dakika içinde geçerliliğini yitirecektir.

Eğer bu talebi siz yapmadıysanız, bu e-postayı dikkate almayınız.

Kargo İşletme Sistemi
Kocaeli Üniversitesi - Yazlab 3
"""

            html_body = f"""
<html>
<head>
    <meta charset=\"UTF-8\">
</head>
<body style=\"font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;\">
    <div style=\"max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);\">
        <div style=\"background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px; text-align: center;\">
            <h1 style=\"color: white; margin: 0; font-size: 24px;\">🔐 Şifre Sıfırlama</h1>
        </div>
        <div style=\"padding: 30px;\">
            <p style=\"color: #333; font-size: 16px;\">Merhaba <strong>{username}</strong>,</p>
            <p style=\"color: #666; font-size: 14px;\">Şifre sıfırlama talebiniz alındı. Aşağıdaki kodu kullanarak yeni şifrenizi belirleyebilirsiniz:</p>
            <div style=\"background: #f8f9fa; border: 2px dashed #667eea; border-radius: 10px; padding: 20px; text-align: center; margin: 25px 0;\">
                <span style=\"font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #667eea;\">{code}</span>
            </div>
            <p style=\"color: #999; font-size: 12px; text-align: center;\">
                ⏱️ Bu kod <strong>15 dakika</strong> içinde geçerliliğini yitirecektir.
            </p>
            <hr style=\"border: none; border-top: 1px solid #eee; margin: 25px 0;\">
            <p style=\"color: #999; font-size: 11px; text-align: center;\">
                Eğer bu talebi siz yapmadıysanız, bu e-postayı dikkate almayınız.<br>
                <strong>Kargo İşletme Sistemi</strong> - Kocaeli Üniversitesi Yazlab 3
            </p>
        </div>
    </div>
</body>
</html>
"""

            part1 = MIMEText(text_body, 'plain', 'utf-8')
            part2 = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"E-posta gönderilemedi: {e}")
            return False
    
    def handle_get_users(self):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password, role, created_at FROM users ORDER BY id")
        users = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        self.send_json(users)
    
    def handle_get_reset_codes(self):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rc.id, rc.user_id, rc.code, rc.created_at, rc.expires_at, rc.used, u.username FROM password_reset_codes rc LEFT JOIN users u ON rc.user_id = u.id ORDER BY rc.created_at DESC"
            )
            codes = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            for code in codes:
                if code.get('created_at'):
                    code['created_at'] = str(code['created_at'])
                if code.get('expires_at'):
                    code['expires_at'] = str(code['expires_at'])
            
            self.send_json(codes)
        except Exception as e:
            print(f"Reset codes hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': f'Veritabanı hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    
    def handle_get_my_route(self):
        session = self.get_session()
        if not session:
            self.send_json({'error': 'Giriş yapmanız gerekiyor'}, 401)
            return
        
        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)
        cargo_id = query_params.get('cargo_id', [None])[0]
        if cargo_id:
            cargo_id = int(cargo_id)
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        
        if cargo_id:
            cursor.execute(
                "SELECT DISTINCT r.id, r.vehicle_id, r.route_data, r.total_distance, r.total_cost, r.created_at, v.name as vehicle_name, v.capacity as vehicle_capacity FROM routes r LEFT JOIN vehicles v ON r.vehicle_id = v.id JOIN route_cargos rc ON r.id = rc.route_id JOIN cargos c ON rc.cargo_id = c.id WHERE c.id = %s AND c.user_id = %s",
                (cargo_id, session['user_id'])
            )
        else:
            cursor.execute(
                "SELECT DISTINCT r.id, r.vehicle_id, r.route_data, r.total_distance, r.total_cost, r.created_at, v.name as vehicle_name, v.capacity as vehicle_capacity FROM routes r LEFT JOIN vehicles v ON r.vehicle_id = v.id JOIN route_cargos rc ON r.id = rc.route_id JOIN cargos c ON rc.cargo_id = c.id WHERE c.user_id = %s",
                (session['user_id'],)
            )
        
        routes = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        self.send_json(routes)
    
    def handle_solve_vrp(self):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        # POST verisini al
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
        except Exception:
            self.send_json({'error': 'Geçersiz veri formatı'}, 400)
            return
        
        scenarios_data = data.get('scenarios', [])
        problem_type = data.get('type', 'limited')
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM stations WHERE is_active=1")
        stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM vehicles WHERE is_owned=1")
        vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM parameters WHERE id=1")
        params_row = cursor.fetchone()
        params = dict_from_row(cursor, params_row) if params_row else {'cost_per_km': 1.0, 'rental_cost': 200, 'rental_capacity': 500}
        
        results = []
        
        for scenario_num, scenario in enumerate(scenarios_data, 1):
            cargos = []
            cargo_id = 1
            for item in scenario:
                station = next((s for s in stations if item['district'] in s['name']), None)
                if station and item['count'] > 0:
                    avg_weight = item['weight'] / item['count']
                    for _ in range(item['count']):
                        cargos.append({
                            'id': cargo_id,
                            'station_id': station['id'],
                            'weight': avg_weight,
                            'station_name': station['name']
                        })
                        cargo_id += 1
            
            if cargos:
                optimizer = RouteOptimizer(stations, cargos, vehicles, params, 'balanced')
                
                if problem_type == 'unlimited':
                    result = optimizer.solve_unlimited_vehicles()
                else:
                    result = optimizer.solve_limited_vehicles()
                
                undelivered_reason = ''
                undelivered = result.get('undelivered', [])
                if undelivered:
                    total_vehicle_capacity = sum(v['capacity'] for v in vehicles)
                    total_cargo_weight = sum(c['weight'] for c in cargos)
                    if problem_type == 'limited' and total_cargo_weight > total_vehicle_capacity:
                        undelivered_reason = f'Kapasite yetersiz ({total_vehicle_capacity}kg < {total_cargo_weight}kg)'
                    else:
                        max_vehicle_cap = max(v['capacity'] for v in vehicles) if vehicles else 0
                        heavy = [c for c in undelivered if c['weight'] > max_vehicle_cap]
                        if heavy:
                            undelivered_reason = f'Kargo cok agir (max: {max_vehicle_cap}kg)'
                        else:
                            undelivered_reason = 'Arac kapasitesi yetersiz'
                
                results.append({
                    'scenario': scenario_num,
                    'problem_type': problem_type,
                    'optimize_for': 'optimal',
                    'total_cost': round(result['total_cost'], 2),
                    'total_fuel_cost': round(result.get('total_fuel_cost', 0), 2),
                    'total_cargos': result['total_cargos'],
                    'total_weight': result['total_weight'],
                    'vehicle_count': len(result['routes']),
                    'rented_vehicles': result.get('rented_vehicles', 0),
                    'undelivered_count': len(undelivered),
                    'undelivered_reason': undelivered_reason,
                    'undelivered_details': result.get('undelivered_details', []),
                    'routes': [{
                        'vehicle_name': r['vehicle']['name'],
                        'route_names': r['route_names'],
                        'distance': r['distance'],
                        'cost': r['cost'],
                        'weight': r['weight'],
                        'cargo_count': r['cargo_count'],
                        'station_cargo_details': r.get('station_cargo_details', [])
                    } for r in result['routes']]
                })
        
        cursor.close()
        conn.close()
        
        self.send_json({'success': True, 'comparison': results})
    
    def handle_compare_pending(self, data: Dict):
        session = self.get_session()
        if not session or session['role'] != 'admin':
            self.send_json({'error': 'Yetkiniz yok'}, 403)
            return
        
        problem_type = data.get('type', data.get('problem_type', 'limited'))
        _delivery_date = data.get('delivery_date')
        cargo_ids = data.get('cargo_ids', [])
        
        conn = get_db()
        if not conn:
            self.send_json({'error': 'Veritabanı hatası'}, 500)
            return
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM stations WHERE is_active=1")
            stations = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM vehicles WHERE is_owned=1")
            vehicles = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            cursor.execute("SELECT * FROM parameters WHERE id=1")
            params_row = cursor.fetchone()
            params = dict_from_row(cursor, params_row) if params_row else {'cost_per_km': 1.0, 'rental_cost': 200, 'rental_capacity': 500}
            
            if cargo_ids and len(cargo_ids) > 0:
                placeholders = ','.join(['%s'] * len(cargo_ids))
                query = "SELECT c.*, s.name as station_name, s.latitude, s.longitude FROM cargos c JOIN stations s ON c.station_id = s.id WHERE c.id IN (" + placeholders + ")"
                cursor.execute(query, tuple(cargo_ids))
                cargos = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            else:
                cursor.execute("SELECT c.*, s.name as station_name, s.latitude, s.longitude FROM cargos c JOIN stations s ON c.station_id = s.id WHERE c.status='pending'")
                cargos = [dict_from_row(cursor, row) for row in cursor.fetchall()]
            
            if not cargos:
                self.send_json({'error': 'Bekleyen kargo yok'}, 404)
                return
            
            results = []
            
            for opt_type in ['distance', 'cost', 'balanced']:
                try:
                    optimizer = RouteOptimizer(stations, cargos, vehicles, params, opt_type)
                    
                    if problem_type == 'unlimited':
                        result = optimizer.solve_unlimited_vehicles()
                    else:
                        result = optimizer.solve_limited_vehicles()
                    
                    results.append({
                        'problem_type': problem_type,
                        'optimize_for': opt_type,
                        'total_cost': round(result['total_cost'], 2),
                        'total_fuel_cost': round(result.get('total_fuel_cost', 0), 2),
                        'total_cargos': result['total_cargos'],
                        'total_weight': result['total_weight'],
                        'vehicle_count': len(result['routes']),
                        'rented_vehicles': result.get('rented_vehicles', 0),
                        'undelivered_count': len(result.get('undelivered', [])),
                        'routes': [{
                            'vehicle_name': r['vehicle']['name'],
                            'route_names': r['route_names'],
                            'distance': r['distance'],
                            'cost': r['cost'],
                            'weight': r['weight'],
                            'cargo_count': r['cargo_count']
                        } for r in result['routes']]
                    })
                except Exception as opt_error:
                    print(f"Optimizasyon hatası (mode {opt_type}): {opt_error}")
                    import traceback
                    traceback.print_exc()
                    results.append({
                        'problem_type': problem_type,
                        'optimize_for': opt_type,
                        'error': str(opt_error),
                        'total_cost': 0,
                        'total_cargos': 0,
                        'total_weight': 0,
                        'vehicle_count': 0,
                        'undelivered_count': len(cargos)
                    })
            
            self.send_json({'success': True, 'comparison': results, 'cargo_count': len(cargos)})
        except Exception as e:
            print(f"Karşılaştırma hatası: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'error': f'Karşılaştırma hatası: {str(e)}'}, 500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


if __name__ == '__main__':
    print("Veritabanı başlatılıyor...")
    success = init_database()
    if not success:
        print("UYARI: Veritabanı başlatılamadı (muhtemelen MySQL kimlik bilgileri). Lütfen `DB_CONFIG` veya `DB_PASSWORD` ortam değişkenini kontrol edin.")
    else:
        print("Veritabanı hazır!")

    print("Sunucu başlatılıyor: http://localhost:8000")
    server = HTTPServer(('localhost', 8000), KargoHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
        server.shutdown()

