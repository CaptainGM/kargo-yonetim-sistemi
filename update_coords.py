import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASSWORD', ''),
    database=os.environ.get('DB_NAME', 'kargo_sistemi'),
)
cursor = conn.cursor()


updates = [
    ("Başiskele", 40.714025, 29.928362),
    ("Çayırova", 40.8261, 29.3711),
    ("Darıca", 40.7692, 29.3753),
    ("Derince", 40.7550, 29.8314),
    ("Dilovası", 40.7833, 29.5333),
    ("Gebze", 40.8027, 29.4307),
    ("Gölcük", 40.72, 29.82),
    ("Kandıra", 41.0711, 30.1528),
    ("Karamürsel", 40.6917, 29.6167),
    ("Kartepe", 40.7533, 30.0224),
    ("Körfez", 40.762527, 29.777346),
    ("İzmit", 40.7654, 29.9408),
]

for name, lat, lon in updates:
    cursor.execute("UPDATE stations SET latitude=%s, longitude=%s WHERE name=%s", (lat, lon, name))
    print(f"{name} güncellendi: {cursor.rowcount} satır")

conn.commit()
print("Tüm koordinatlar başarıyla güncellendi!")

cursor.close()
conn.close()
