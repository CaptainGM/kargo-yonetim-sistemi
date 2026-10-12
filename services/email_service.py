# -*- coding: utf-8 -*-
"""
E-posta Gönderim Servisi (SMTP & Şifre Sıfırlama)
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from config import EMAIL_CONFIG


def send_reset_email(to_email: str, username: str, code: str) -> bool:
    """
    Kullanıcıya 6 haneli şifre sıfırlama kodunu HTML şablonlu e-posta ile iletir.
    SMTP yapılandırılmamışsa False döner; geliştirme ortamında kod loglanır.
    """
    sender_email = EMAIL_CONFIG.get('sender_email', '')
    sender_password = EMAIL_CONFIG.get('sender_password', '')
    
    if not sender_email or not sender_password:
        print(f"[SMTP DEV] E-posta yapılandırılmamış. Şifre sıfırlama kodu [{username} -> {to_email}]: {code}")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Şifre Sıfırlama Kodu - {EMAIL_CONFIG.get('sender_name', 'Kargo Sistemi')}"
        msg['From'] = f"{EMAIL_CONFIG.get('sender_name', 'Kargo Sistemi')} <{sender_email}>"
        msg['To'] = to_email

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }}
                .card {{ max-width: 500px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
                .header {{ text-align: center; border-bottom: 2px solid #eef2f7; padding-bottom: 20px; }}
                .title {{ color: #1e293b; font-size: 22px; font-weight: 700; margin: 0; }}
                .code-box {{ background: linear-gradient(135deg, #6366f1, #4f46e5); color: #ffffff; font-size: 32px; font-weight: 800; letter-spacing: 6px; text-align: center; padding: 18px; border-radius: 8px; margin: 25px 0; }}
                .footer {{ font-size: 12px; color: #94a3b8; text-align: center; margin-top: 25px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h2 class="title">Şifre Sıfırlama Talebi</h2>
                </div>
                <p>Merhaba <strong>{username}</strong>,</p>
                <p>Hesabınız için şifre sıfırlama talebinde bulundunuz. Aşağıdaki 6 haneli doğrulama kodunu kullanarak yeni şifrenizi belirleyebilirsiniz:</p>
                <div class="code-box">{code}</div>
                <p>Bu kod <strong>15 dakika</strong> boyunca geçerlidir. Talebi siz yapmadıysanız bu mesajı görmezden gelebilirsiniz.</p>
                <div class="footer">
                    &copy; LogiRoute Lojistik & Kargo Rota Yönetim Sistemi
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"[OK] Şifre sıfırlama kodu {to_email} adresine iletildi.")
        return True
    except Exception as e:
        print(f"[X] E-posta gönderim hatası: {e}")
        return False
