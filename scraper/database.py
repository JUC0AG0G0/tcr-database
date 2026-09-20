import os
import psycopg2

DB_HOST = os.getenv("DB_HOST", "tcr_db_dev")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "tcr_database")
DB_USER = os.getenv("POSTGRES_USER", "tcr_admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "tcr_password")

def get_connection():
    try:
        return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    except Exception as e:
        print(f"❌ Erreur BDD : {e}")
        return None

# --- ENTITÉS DE BASE ---
def get_or_create_driver(conn, first_name, last_name):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM drivers WHERE "firstName" = %s AND "lastName" = %s', (first_name, last_name))
    res = cursor.fetchone()
    if res: return res[0]
    cursor.execute('INSERT INTO drivers ("firstName", "lastName") VALUES (%s, %s) RETURNING id', (first_name, last_name))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

def get_or_create_team(conn, name):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM teams WHERE name = %s', (name,))
    res = cursor.fetchone()
    if res: return res[0]
    cursor.execute('INSERT INTO teams (name) VALUES (%s) RETURNING id', (name,))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

def get_or_create_car(conn, brand, model):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM cars WHERE brand = %s AND model = %s', (brand, model))
    res = cursor.fetchone()
    if res: return res[0]
    cursor.execute('INSERT INTO cars (brand, model) VALUES (%s, %s) RETURNING id', (brand, model))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

# --- ARBORESCENCE ---
def get_or_create_hierarchy(conn):
    """Crée l'arborescence (WTCR > 2018 > Maroc > Course 1) et renvoie l'ID de la Session"""
    cursor = conn.cursor()
    
    # 1. Championnat
    cursor.execute("SELECT id FROM championships WHERE name = 'WTCR'")
    res = cursor.fetchone()
    champ_id = res[0] if res else cursor.execute("INSERT INTO championships (name, region) VALUES ('WTCR', 'Global') RETURNING id") or cursor.fetchone()[0]
    
    # 2. Saison
    cursor.execute('SELECT id FROM seasons WHERE year = 2018 AND "championshipId" = %s', (champ_id,))
    res = cursor.fetchone()
    season_id = res[0] if res else cursor.execute('INSERT INTO seasons (year, "championshipId") VALUES (2018, %s) RETURNING id', (champ_id,)) or cursor.fetchone()[0]
    
    # 3. Événement
    cursor.execute('SELECT id FROM events WHERE name = %s AND "seasonId" = %s', ('Race of Morocco', season_id))
    res = cursor.fetchone()
    event_id = res[0] if res else cursor.execute('INSERT INTO events (name, circuit, "seasonId") VALUES (%s, %s, %s) RETURNING id', ('Race of Morocco', 'Circuit Moulay el Hassan', season_id)) or cursor.fetchone()[0]
    
    # 4. Session
    cursor.execute('SELECT id FROM sessions WHERE name = %s AND "eventId" = %s', ('Race 1', event_id))
    res = cursor.fetchone()
    session_id = res[0] if res else cursor.execute('INSERT INTO sessions (name, type, "eventId") VALUES (%s, %s, %s) RETURNING id', ('Race 1', 'RACE', event_id)) or cursor.fetchone()[0]
    
    conn.commit()
    return session_id

# --- SAUVEGARDE DU RÉSULTAT ---
def save_result(conn, session_id, driver_id, team_id, car_id, position, laps, time_or_gap):
    cursor = conn.cursor()
    
    # Traitement du Statut (Abandon, Fini, etc.)
    status = "Finished"
    finish_pos = None
    if position.isdigit():
        finish_pos = int(position)
    elif position == "R":
        status = "DNF" # Abandon
    elif position in ["DNS", "DSQ"]:
        status = position
        
    # Traitement des tours
    laps_count = int(laps) if laps.isdigit() else None
    
    # Vérification des doublons
    cursor.execute('SELECT id FROM results WHERE "sessionId" = %s AND "driverId" = %s', (session_id, driver_id))
    if cursor.fetchone():
        return # Résultat déjà inséré
        
    # Insertion
    cursor.execute('''
        INSERT INTO results ("sessionId", "driverId", "teamId", "carId", "finishPosition", status, laps, "timeOrGap")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (session_id, driver_id, team_id, car_id, finish_pos, status, laps_count, time_or_gap))
    conn.commit()