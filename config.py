# -*- coding: utf-8 -*-
"""
Kargo & Lojistik Yönetim Sistemi - Yapılandırma Modülü
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# MongoDB Yapılandırması
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'kargo_sistemi')

# Sunucu Yapılandırması
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.environ.get('SERVER_PORT', 8000))

# E-posta (SMTP) Yapılandırması
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', 587)),
    'sender_email': os.environ.get('SENDER_EMAIL', ''),
    'sender_password': os.environ.get('SENDER_PASSWORD', ''),
    'sender_name': os.environ.get('SENDER_NAME', 'LogiRoute Kargo Yönetim Sistemi')
}

# Güvenlik & Oturum
SESSION_COOKIE_NAME = 'session_id'
PASSWORD_SALT = os.environ.get('PASSWORD_SALT', 'logiroute_secure_salt_2026')
