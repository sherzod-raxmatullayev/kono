import sqlite3


DB_NAME = "anime.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()


    # Users jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id TEXT UNIQUE NOT NULL,     
        channel_name TEXT                    
    )
    """)


    # Admin jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL
    )
    """)

    # Anime jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        janr TEXT,
        yili TEXT,
        duber TEXT,
        qisimlari INTEGER DEFAULT 0,
        yuklashlar INTEGER DEFAULT 0,
        yuklangan_sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_id TEXT
    )
    """)

    # Qisimlar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qisimlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        qismi INTEGER NOT NULL,
        anime_id INTEGER NOT NULL,
        file_id TEXT NOT NULL,
        FOREIGN KEY (anime_id) REFERENCES anime (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()



# ----------------- USERS funksiyalari -----------------
def add_user(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  
    conn.close()
    return users

def get_users_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_user_by_telegram(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user


# ----------------- ADMIN funksiyalari -----------------
def add_admin(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO admin (telegram_id) VALUES (?)", (telegram_id,))
    conn.commit()
    conn.close()

def get_admin_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_admin_by_telegram(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE telegram_id = ?", (telegram_id,))
    admin = cursor.fetchone()
    conn.close()
    return admin

def get_all_admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    conn.close()
    return  admins


def get_all_admin_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    conn.close()
    return [admin[1] for admin in admins]  



def delete_admin(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()


# ----------------- ANIME funksiyalari -----------------
def add_anime(name: str, janr: str, yili: str, duber: str, qisimlari: int, file_id: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO anime (name, janr, yili, duber, qisimlari, file_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, janr, yili, duber, qisimlari, file_id))
    
    anime_id = cursor.lastrowid  # ID ni shu yerda olamiz
    
    conn.commit()
    conn.close()
    
    return anime_id

def get_anime_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM anime")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_anime_by_id(anime_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    anime = cursor.fetchone()
    conn.close()
    return anime


def get_all_anime():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anime ORDER BY id DESC")
    animes = cursor.fetchall()
    conn.close()
    return animes


def update_anime_views(anime_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE anime SET yuklashlar = yuklashlar + 1 WHERE id = ?", (anime_id,))
    conn.commit()
    conn.close()


def delete_anime(anime_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


# ----------------- QISIMLAR funksiyalari -----------------
def add_qism(anime_id: int, file_id: str, qismi: int) -> int | None:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO qisimlar (anime_id, file_id, qismi) VALUES (?, ?, ?)",
            (anime_id, file_id, qismi)
        )
        qism_id = cursor.lastrowid  # yangi qo'shilgan qatordagi ID

        conn.commit()
        conn.close()
        return qism_id
    except Exception as e:
        print("Xatolik:", e)
        return None



def get_series_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM qisimlar")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def qisimlari(anime_id: int, qismi: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM qisimlar WHERE anime_id = ? AND qismi = ?", (anime_id, qismi))
    qisimlar = cursor.fetchone()
    conn.close()
    return qisimlar

def get_qisimlar_by_anime(anime_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM qisimlar WHERE anime_id = ? ORDER BY qismi ASC",
        (anime_id,)
    )
    qisimlar = cursor.fetchall()
    conn.close()
    return qisimlar

def get_qism_by_id(qism_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM qisimlar WHERE id = ?", (qism_id,))
        qism = cursor.fetchone()
        conn.close()
        return qism  # tuple yoki None qaytadi
    except:
        return None


def delete_qism(qism_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM qisimlar WHERE id = ?", (qism_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


# ----------------- MAXSUS FUNKSIYALAR -----------------
def get_top_10_anime():
    """Eng ko‘p yuklangan 10 ta anime"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM anime
        ORDER BY yuklashlar DESC
        LIMIT 10
    """)
    animes = cursor.fetchall()
    conn.close()
    return animes


def get_latest_anime(limit: int = 10):
    """Oxirgi yuklangan animelar (default 10 ta)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM anime
        ORDER BY yuklangan_sana DESC
        LIMIT ?
    """, (limit,))
    animes = cursor.fetchall()
    conn.close()
    return animes

import json

def get_anime_json(anime_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
    anime = cursor.fetchone()
    conn.close()

    if anime is None:
        return None

    # Bazadagi ustunlarni olish tartibi
    anime_dict = {
        "id": anime[0],
        "name": anime[1],
        "janr": anime[2],
        "yili": anime[3],
        "duber": anime[4],
        "qisimlari": anime[5],
        "yuklashlar": anime[6],
        "yuklangan_sana": anime[7],
        "file_id": anime[8]
    }

    # Chiroyli text (emoji va bezaklar bilan)
    text = (
        f"🎬 {anime_dict['name']}\n"
        f"📌 Janr: {anime_dict['janr'] or 'Noma’lum'}\n"
        f"📅 Yili: {anime_dict['yili'] or 'Noma’lum'}\n"
        f"🎙 Duber: {anime_dict['duber'] or 'Noma’lum'}\n"
        f"📂 Qismlar: {anime_dict['qisimlari']}\n"
        f"⬇ Yuklashlar: {anime_dict['yuklashlar']}\n"
        f"⏰ Yuklangan sana: {anime_dict['yuklangan_sana']}"
    )

    # JSON formatida qaytaramiz
    return {
        "file_id": anime_dict["file_id"] or "",
        "text": text
    }


# ----------------- SUBSCRIPTIONS funksiyalari -----------------
def add_subscription(channel_id: str, channel_name: str = None):
    try:
        """Majburiy obuna kanal qo‘shish"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO subscriptions (channel_id, channel_name)
            VALUES (?, ?)
        """, (channel_id, channel_name))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def get_all_subscriptions():
    """Barcha majburiy obuna kanallarini olish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions ORDER BY id")
    channels = cursor.fetchall()
    conn.close()
    return channels

def get_channels_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM subscriptions")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_subscription_by_id(sub_id: int):
    """Bitta obuna kanalini olish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscriptions WHERE id = ?", (sub_id,))
    channel = cursor.fetchone()
    conn.close()
    return channel


def delete_subscription(sub_id: int):
    try:
        """Obuna kanalini o‘chirish"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
        conn.commit()
        conn.close()
        return True
    except:
        return False


    