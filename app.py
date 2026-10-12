# -*- coding: utf-8 -*-
"""
Kargo & Lojistik Rota Yönetim Sistemi - Ana Uygulama Sunucusu
Çok iş parçacıklı (ThreadingHTTPServer) ve MongoDB tabanlı REST API sunucusu.
"""
import os
import mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from config import SERVER_HOST, SERVER_PORT, BASE_DIR
from database import init_database
from handlers.base_handler import BaseHandler

# API Modülleri
from handlers.auth_handlers import (
    handle_session, handle_login, handle_logout,
    handle_register, handle_forgot_password, handle_reset_password
)
from handlers.station_handlers import (
    handle_get_stations, handle_add_station, handle_delete_station
)
from handlers.vehicle_handlers import (
    handle_get_vehicles, handle_add_vehicle, handle_delete_vehicle
)
from handlers.cargo_handlers import (
    handle_get_cargos, handle_add_cargo, handle_delete_cargo, handle_get_my_route
)
from handlers.route_handlers import (
    handle_get_routes, handle_delete_route, handle_route_geometry
)
from handlers.optimize_handlers import (
    handle_optimize, handle_load_scenario,
    handle_compare_scenarios, handle_compare_pending
)
from handlers.admin_handlers import (
    handle_get_parameters, handle_update_parameters,
    handle_get_stats, handle_get_db_stats, handle_get_db_data,
    handle_get_users, handle_delete_user, handle_get_reset_codes,
    handle_market_fuel_check, handle_live_weather
)


class KargoRequestHandler(SimpleHTTPRequestHandler):
    """
    Tüm HTTP isteklerini yönlendiren REST API & Statik Dosya İşleyicisi
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        """Temiz sunucu log formatı."""
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} - {args[0]}")

    def do_OPTIONS(self):
        """CORS ön denetim (pre-flight) yanıtı."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Cookie')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # REST API Rotaları
        if path == '/api/session':
            handle_session(self)
        elif path == '/api/stations':
            handle_get_stations(self)
        elif path == '/api/vehicles':
            handle_get_vehicles(self)
        elif path == '/api/cargos':
            handle_get_cargos(self)
        elif path == '/api/routes':
            handle_get_routes(self)
        elif path == '/api/my-route':
            handle_get_my_route(self)
        elif path == '/api/parameters':
            handle_get_parameters(self)
        elif path == '/api/stats':
            handle_get_stats(self)
        elif path == '/api/users':
            handle_get_users(self)
        elif path == '/api/reset-codes':
            handle_get_reset_codes(self)
        elif path == '/api/db-stats':
            handle_get_db_stats(self)
        elif path == '/api/db-data':
            handle_get_db_data(self)
        elif path == '/api/live-weather':
            handle_live_weather(self)

        # HTML Sayfa Rotaları
        elif path in ('/', '/index.html'):
            self.serve_html_file('templates/index.html')
        elif path in ('/db-view', '/database', '/db-view.html'):
            self.serve_html_file('templates/db-view.html')

        # Statik Dosyalar (/static/...)
        elif path.startswith('/static/'):
            self.serve_static_asset(path)
        else:
            # Diğer dosyalar için SimpleHTTPRequestHandler fallback
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        data = BaseHandler.get_json_body(self)

        if path == '/api/login':
            handle_login(self, data)
        elif path == '/api/logout':
            handle_logout(self)
        elif path == '/api/register':
            handle_register(self, data)
        elif path == '/api/forgot-password':
            handle_forgot_password(self, data)
        elif path == '/api/reset-password':
            handle_reset_password(self, data)
        elif path == '/api/stations':
            handle_add_station(self, data)
        elif path == '/api/vehicles':
            handle_add_vehicle(self, data)
        elif path == '/api/cargos':
            handle_add_cargo(self, data)
        elif path == '/api/load-scenario':
            handle_load_scenario(self, data)
        elif path == '/api/optimize':
            handle_optimize(self, data)
        elif path == '/api/compare-scenarios':
            handle_compare_scenarios(self, data)
        elif path == '/api/compare-pending':
            handle_compare_pending(self, data)
        elif path == '/api/route-geometry':
            handle_route_geometry(self, data)
        elif path == '/api/market-fuel-check':
            handle_market_fuel_check(self, data)
        else:
            BaseHandler.send_json(self, {'error': f'Geçersiz POST endpoint: {path}'}, 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path
        data = BaseHandler.get_json_body(self)

        if path == '/api/parameters':
            handle_update_parameters(self, data)
        else:
            BaseHandler.send_json(self, {'error': f'Geçersiz PUT endpoint: {path}'}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith('/api/stations/'):
            sid = int(path.split('/')[-1])
            handle_delete_station(self, sid)
        elif path.startswith('/api/users/'):
            uid = int(path.split('/')[-1])
            handle_delete_user(self, uid)
        elif path.startswith('/api/cargos/'):
            cid = int(path.split('/')[-1])
            handle_delete_cargo(self, cid)
        elif path.startswith('/api/vehicles/'):
            vid = int(path.split('/')[-1])
            handle_delete_vehicle(self, vid)
        elif path.startswith('/api/routes/'):
            rid = int(path.split('/')[-1])
            handle_delete_route(self, rid)
        else:
            BaseHandler.send_json(self, {'error': f'Geçersiz DELETE endpoint: {path}'}, 404)

    def serve_html_file(self, rel_path: str):
        """HTML şablon dosyasını UTF-8 olarak okur ve sunar."""
        full_path = os.path.join(str(BASE_DIR), rel_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(404, f'Sayfa bulunamadı: {e}')

    def serve_static_asset(self, rel_path: str):
        """Statik varlıkları doğru MIME tipi ve önbellek başlığı ile sunar."""
        clean_path = rel_path.lstrip('/')
        full_path = os.path.join(str(BASE_DIR), clean_path)

        if not os.path.exists(full_path):
            self.send_error(404, 'Statik dosya bulunamadı')
            return

        mime_type, _ = mimetypes.guess_type(full_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f'Statik dosya okuma hatası: {e}')


def run_server():
    """MongoDB'yi başlatır ve ThreadingHTTPServer'ı ayağa kaldırır."""
    print("=" * 60)
    print("  LOGIROUTE - Kargo & Lojistik Rota Yönetim Platformu")
    print("  Çok İş Parçacıklı Sunucu & MongoDB Mimarisi")
    print("=" * 60)

    # 1. MongoDB Başlatma
    db_ready = init_database()
    if not db_ready:
        print("[!] UYARI: MongoDB bağlantısı kurulamadı. Lütfen MongoDB servisinin açık olduğundan emin olun.")
    else:
        print("[OK] MongoDB hazır ve yapılandırıldı.")

    # 2. HTTP Sunucusu Başlatma
    server_address = (SERVER_HOST, SERVER_PORT)
    server = ThreadingHTTPServer(server_address, KargoRequestHandler)
    print(f"\n[+] Sunucu aktif: http://localhost:{SERVER_PORT}")
    print(f"[+] Veritabanı Görüntüleyici: http://localhost:{SERVER_PORT}/db-view")
    print(f"[*] Durdurmak için CTRL+C tuşlarına basabilirsiniz.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Sunucu güvenli şekilde kapatılıyor...")
        server.shutdown()


if __name__ == '__main__':
    run_server()
