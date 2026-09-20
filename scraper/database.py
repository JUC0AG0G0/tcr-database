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
# --- ARBORESCENCE ---
def get_or_create_hierarchy(conn, champ_name, year, event_name, circuit, start_date=None, end_date=None, session_name="Race 1", session_type="RACE", session_date=None):
    """Crée l'arborescence dynamique et met à jour les dates si elles sont fournies."""
    cursor = conn.cursor()
    
    # 1. Championnat
    cursor.execute('SELECT id FROM championships WHERE name = %s', (champ_name,))
    res = cursor.fetchone()
    champ_id = res[0] if res else cursor.execute("INSERT INTO championships (name, region) VALUES (%s, 'Global') RETURNING id", (champ_name,)) or cursor.fetchone()[0]
    
    # 2. Saison
    cursor.execute('SELECT id FROM seasons WHERE year = %s AND "championshipId" = %s', (year, champ_id))
    res = cursor.fetchone()
    season_id = res[0] if res else cursor.execute('INSERT INTO seasons (year, "championshipId") VALUES (%s, %s) RETURNING id', (year, champ_id)) or cursor.fetchone()[0]
    
    # 3. Événement
    cursor.execute('SELECT id FROM events WHERE name = %s AND "seasonId" = %s', (event_name, season_id))
    res = cursor.fetchone()
    if res:
        event_id = res[0]
        # Si l'événement existe mais qu'on a de nouvelles dates, on met à jour !
        if start_date and end_date:
            cursor.execute('UPDATE events SET "startDate" = %s, "endDate" = %s WHERE id = %s', (start_date, end_date, event_id))
    else:
        cursor.execute('''
            INSERT INTO events (name, circuit, "startDate", "endDate", "seasonId") 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        ''', (event_name, circuit, start_date, end_date, season_id))
        event_id = cursor.fetchone()[0]
    
    # 4. Session
    cursor.execute('SELECT id FROM sessions WHERE name = %s AND "eventId" = %s', (session_name, event_id))
    res = cursor.fetchone()
    if res:
        session_id = res[0]
        # Idem, on met à jour la date de la session
        if session_date:
            cursor.execute('UPDATE sessions SET date = %s WHERE id = %s', (session_date, session_id))
    else:
        cursor.execute('''
            INSERT INTO sessions (name, type, date, "eventId") 
            VALUES (%s, %s, %s, %s) RETURNING id
        ''', (session_name, session_type, session_date, event_id))
        session_id = cursor.fetchone()[0]
    
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