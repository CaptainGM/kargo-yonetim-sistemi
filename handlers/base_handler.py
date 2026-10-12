# -*- coding: utf-8 -*-
"""
Kargo Yönetim Sistemi - Temel HTTP İşleyici ve Oturum Yönetimi
"""
import json
import uuid
from typing import Any, Dict, Optional
from database import serialize_doc, serialize_docs

# Bellek içi oturum deposu (isteğe bağlı MongoDB ile senkronize)
sessions: Dict[str, Dict] = {}


class BaseHandler:
    @staticmethod
    def send_json(handler, data: Any, status: int = 200):
        """JSON yanıtını uygun başlıklar ve UTF-8 karakter kümesi ile istemciye gönderir."""
        handler.send_response(status)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Cookie')
        handler.end_headers()
        json_str = json.dumps(data, ensure_ascii=False, default=str)
        handler.wfile.write(json_str.encode('utf-8'))

    @staticmethod
    def get_json_body(handler) -> Dict:
        """HTTP istek gövdesindeki (body) JSON verisini ayrıştırır."""
        try:
            content_length = int(handler.headers.get('Content-Length', 0))
            if content_length > 0:
                raw_body = handler.rfile.read(content_length).decode('utf-8')
                return json.loads(raw_body)
        except Exception:
            pass
        return {}

    @staticmethod
    def get_session(handler) -> Optional[Dict]:
        """İstek çerezlerinden oturum bilgisini çeker."""
        cookie_header = handler.headers.get('Cookie', '')
        for part in cookie_header.split(';'):
            if 'session_id=' in part:
                session_id = part.split('=')[1].strip()
                return sessions.get(session_id)
        return None

    @staticmethod
    def set_session(handler, user_data: Dict) -> str:
        """Kullanıcı için yeni bir oturum başlatır ve session_id döner."""
        session_id = str(uuid.uuid4())
        sessions[session_id] = user_data
        return session_id

    @staticmethod
    def clear_session(handler):
        """Mevcut oturumu sonlandırır."""
        cookie_header = handler.headers.get('Cookie', '')
        for part in cookie_header.split(';'):
            if 'session_id=' in part:
                session_id = part.split('=')[1].strip()
                if session_id in sessions:
                    del sessions[session_id]
