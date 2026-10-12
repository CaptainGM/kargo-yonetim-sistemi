# -*- coding: utf-8 -*-
"""
Kullanıcı Girişi, Kayıt ve Şifre Sıfırlama İşleyicileri
"""
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict

from database import get_db, get_next_id
from handlers.base_handler import BaseHandler
from services.email_service import send_reset_email


def handle_session(handler):
    session = BaseHandler.get_session(handler)
    if session:
        BaseHandler.send_json(handler, {
            'logged_in': True,
            'user_id': session['user_id'],
            'username': session['username'],
            'role': session['role']
        })
    else:
        BaseHandler.send_json(handler, {'logged_in': False})


def handle_login(handler, data: Dict):
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        BaseHandler.send_json(handler, {'error': 'Kullanıcı adı ve şifre zorunludur'}, 400)
        return

    db = get_db()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = db.users.find_one({'username': username, 'password': password_hash})

    if user:
        user_id = user['id']
        role = user.get('role', 'user')
        session_id = BaseHandler.set_session(handler, {
            'user_id': user_id,
            'username': username,
            'role': role
        })

        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; SameSite=Lax')
        handler.end_headers()
        import json
        handler.wfile.write(json.dumps({
            'success': True,
            'role': role,
            'username': username,
            'user_id': user_id
        }, ensure_ascii=False).encode('utf-8'))
    else:
        BaseHandler.send_json(handler, {'error': 'Geçersiz kullanıcı adı veya şifre'}, 401)


def handle_logout(handler):
    BaseHandler.clear_session(handler)
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Set-Cookie', 'session_id=; Path=/; Max-Age=0')
    handler.end_headers()
    import json
    handler.wfile.write(json.dumps({'success': True}).encode('utf-8'))


def handle_register(handler, data: Dict):
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        BaseHandler.send_json(handler, {'error': 'Tüm alanları doldurunuz'}, 400)
        return

    db = get_db()
    if db.users.find_one({'username': username}):
        BaseHandler.send_json(handler, {'error': 'Bu kullanıcı adı zaten mevcut'}, 400)
        return

    if db.users.find_one({'email': email}):
        BaseHandler.send_json(handler, {'error': 'Bu e-posta adresi zaten kayıtlı'}, 400)
        return

    uid = get_next_id('users')
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db.users.insert_one({
        'id': uid,
        'username': username,
        'email': email,
        'password': password_hash,
        'plain_password': password,
        'role': 'user',
        'created_at': datetime.now()
    })

    BaseHandler.send_json(handler, {'success': True, 'message': 'Kayıt başarılı'})


def handle_forgot_password(handler, data: Dict):
    email = data.get('email', '').strip()
    if not email:
        BaseHandler.send_json(handler, {'error': 'E-posta adresi gerekli'}, 400)
        return

    db = get_db()
    user = db.users.find_one({'email': email})
    if not user:
        BaseHandler.send_json(handler, {'error': 'Bu e-posta adresi kayıtlı değil'}, 404)
        return

    user_id = user['id']
    username = user['username']
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = datetime.now() + timedelta(minutes=15)

    db.password_reset_codes.delete_many({'user_id': user_id})
    db.password_reset_codes.insert_one({
        'id': get_next_id('password_reset_codes'),
        'user_id': user_id,
        'email': email,
        'code': code,
        'created_at': datetime.now(),
        'expires_at': expires_at,
        'used': 0
    })

    sent = send_reset_email(email, username, code)
    if sent:
        BaseHandler.send_json(handler, {
            'success': True,
            'message': 'Doğrulama kodu e-posta adresinize gönderildi'
        })
    else:
        BaseHandler.send_json(handler, {
            'success': True,
            'message': f'Doğrulama kodunuz: {code} (E-posta sunucusu bağlı değil)',
            'code': code
        })


def handle_reset_password(handler, data: Dict):
    email = data.get('email', '').strip()
    code = data.get('code', '').strip()
    new_password = data.get('new_password', '')

    if not email or not code or not new_password:
        BaseHandler.send_json(handler, {'error': 'Tüm alanları doldurunuz'}, 400)
        return

    db = get_db()
    user = db.users.find_one({'email': email})
    if not user:
        BaseHandler.send_json(handler, {'error': 'Geçersiz e-posta adresi'}, 400)
        return

    user_id = user['id']
    reset_record = db.password_reset_codes.find_one({
        'user_id': user_id,
        'code': code,
        'used': 0,
        'expires_at': {'$gt': datetime.now()}
    })

    if not reset_record:
        BaseHandler.send_json(handler, {'error': 'Geçersiz veya süresi dolmuş kod'}, 400)
        return

    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    db.users.update_one(
        {'id': user_id},
        {'$set': {'password': password_hash, 'plain_password': new_password}}
    )
    db.password_reset_codes.update_one(
        {'_id': reset_record['_id']},
        {'$set': {'used': 1}}
    )

    BaseHandler.send_json(handler, {
        'success': True,
        'message': 'Şifreniz başarıyla değiştirildi'
    })
