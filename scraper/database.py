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
        print(f"❌ Erreur de connexion à la BDD : {e}")
        return None

def get_or_create_driver(conn, first_name, last_name):
    cursor = conn.cursor()
    # TypeORM met des guillemets autour des colonnes en camelCase ("firstName")
    cursor.execute('SELECT id FROM drivers WHERE "firstName" = %s AND "lastName" = %s', (first_name, last_name))
    res = cursor.fetchone()
    if res:
        return res[0] # Le pilote existe, on renvoie son ID
    
    # S'il n'existe pas, on le crée
    cursor.execute('INSERT INTO drivers ("firstName", "lastName") VALUES (%s, %s) RETURNING id', (first_name, last_name))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

def get_or_create_team(conn, name):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM teams WHERE name = %s', (name,))
    res = cursor.fetchone()
    if res:
        return res[0]
    
    cursor.execute('INSERT INTO teams (name) VALUES (%s) RETURNING id', (name,))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id

def get_or_create_car(conn, brand, model):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM cars WHERE brand = %s AND model = %s', (brand, model))
    res = cursor.fetchone()
    if res:
        return res[0]
    
    cursor.execute('INSERT INTO cars (brand, model) VALUES (%s, %s) RETURNING id', (brand, model))
    new_id = cursor.fetchone()[0]
    conn.commit()
    return new_id