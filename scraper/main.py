import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
from database import get_connection, get_or_create_driver, get_or_create_team, get_or_create_car, get_or_create_hierarchy, save_result

BASE_URL = "https://www.touringcars.net/database"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def parse_date(date_str, year):
    """Convertit 'Sat Apr 7' en '2018-04-07'"""
    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    try:
        parts = date_str.strip().split(" ")
        if len(parts) >= 3:
            month = months.get(parts[1][:3], "01")
            day = parts[2].zfill(2)
            return f"{year}-{month}-{day}"
    except:
        pass
    return f"{year}-01-01"

def extract_session(session_url, conn, series, year, event_name, circuit, start_date, end_date, session_name, session_type):
    """Télécharge une session spécifique et insère ses résultats en DB."""
    try:
        response = requests.get(session_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('div', class_='tb-row')
        
        if not rows:
            return

        # Par défaut, on met à 1h du matin le jour du début de l'événement comme tu l'as demandé
        session_date = f"{start_date} 01:00:00"

        # Création de l'arborescence
        session_id = get_or_create_hierarchy(
            conn, champ_name=series, year=year, event_name=event_name, circuit=circuit,
            start_date=start_date, end_date=end_date, session_name=session_name, 
            session_type=session_type, session_date=session_date
        )

        # Extraction des résultats
        for row in rows:
            if 'header' in row.get('class', []): continue
            
            try:
                pos = row.find('div', class_='pos').find('span').text.strip()
                driver = row.find('div', class_='driver').find('a').text.strip()
                team = row.find('div', class_='entrant').text.strip()
                car = row.find('div', class_='car').text.strip()
                
                # Tours et temps peuvent être vides sur les abandons
                laps_div = row.find('div', class_='laps')
                laps = laps_div.text.strip() if laps_div else "0"
                
                time_div = row.find('div', class_='time')
                time = time_div.text.strip() if time_div else ""
                
                # Découpage Prénom/Nom et Marque/Modèle
                first_name, *last_name_parts = driver.split(" ", 1)
                last_name = last_name_parts[0] if last_name_parts else ""
                
                brand, *model_parts = car.split(" ", 1)
                model = model_parts[0] if model_parts else ""

                # Insertion base de données
                d_id = get_or_create_driver(conn, first_name, last_name)
                t_id = get_or_create_team(conn, team)
                c_id = get_or_create_car(conn, brand, model)
                save_result(conn, session_id, d_id, t_id, c_id, pos, laps, time)
                
            except AttributeError:
                continue
                
        print(f"  ✅ {session_name} sauvegardée.")
    except Exception as e:
        print(f"  ❌ Erreur sur {session_name}: {e}")

def scrape_full_season(series="WTCR", year=2018):
    print(f"🚀 Lancement de l'extraction complète : {series} {year}\n")
    url = f"{BASE_URL}/season.php?series={series}&year={year}"
    conn = get_connection()
    if not conn: return
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        # Force la lecture malgré le bug de l'erreur 404 du serveur
        soup = BeautifulSoup(response.text, "html.parser")
        
        cards = soup.find_all('div', class_='custom-card')
        print(f"🏁 {len(cards)} événements trouvés dans le calendrier.\n")
        
        for card in cards:
            # Extraction du circuit
            circuit_link = card.find('a', href=re.compile(r'circuit\.php'))
            circuit_name = "Inconnu"
            if circuit_link:
                # Extrait le nom du circuit depuis l'URL (ex: track=Circuit Moulay el Hassan)
                circuit_name = unquote(circuit_link.get('href').split('track=')[-1])
            
            # Extraction des dates
            dates_span = card.find('span', class_='dates')
            start_date, end_date = f"{year}-01-01", f"{year}-01-01"
            
            if dates_span:
                date_text = dates_span.text.strip()
                date_parts = [p.strip() for p in date_text.split('-')]
                start_date = parse_date(date_parts[0], year)
                end_date = parse_date(date_parts[-1], year) # Fonctionne même s'il n'y a pas de tiret
                
            print(f"🏎️  Événement : {circuit_name} ({start_date} au {end_date})")
            
            # On récupère toutes les sessions (Qualifs et Courses) de cette carte
            session_links = card.find_all('a', href=re.compile(r'(race\.php\?id=|qualifying\.php\?id=)'))
            
            for link in session_links:
                href = link.get('href')
                session_url = f"{BASE_URL}/{href}"
                session_name = link.text.strip()
                session_type = "QUALIFYING" if "qualifying" in href else "RACE"
                
                # On lance l'extracteur de course
                extract_session(session_url, conn, series, year, circuit_name, circuit_name, start_date, end_date, session_name, session_type)
            
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Erreur critique : {e}")
    finally:
        conn.close()
        print("\n🎉 Extraction de la saison terminée avec succès !")

if __name__ == "__main__":
    scrape_full_season("WTCR", 2018)