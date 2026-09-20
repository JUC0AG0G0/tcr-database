import requests
from bs4 import BeautifulSoup
from database import get_connection, get_or_create_driver, get_or_create_team, get_or_create_car, get_or_create_hierarchy, save_result

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def extract_race_results(url):
    print(f"Téléchargement de : {url}\n")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('div', class_='tb-row')
        
        results = []
        for row in rows:
            if 'header' in row.get('class', []): continue
            try:
                pos = row.find('div', class_='pos').find('span').text.strip()
                driver = row.find('div', class_='driver').find('a').text.strip()
                team = row.find('div', class_='entrant').text.strip()
                car = row.find('div', class_='car').text.strip()
                laps = row.find('div', class_='laps').text.strip()
                time = row.find('div', class_='time').text.strip()
                results.append({"Pos": pos, "Pilote": driver, "Equipe": team, "Voiture": car, "Tours": laps, "Temps": time})
            except AttributeError:
                continue

        # --- SAUVEGARDE DB ---
        conn = get_connection()
        if not conn: return
        
        # 1. Création de l'arborescence
        session_id = get_or_create_hierarchy(conn)
        print("✅ Arborescence (WTCR 2018 -> Maroc -> Course 1) générée.\n")

        # 2. Insertion des chronos
        for r in results:
            name_parts = r["Pilote"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            car_parts = r["Voiture"].split(" ", 1)
            brand = car_parts[0]
            model = car_parts[1] if len(car_parts) > 1 else ""

            d_id = get_or_create_driver(conn, first_name, last_name)
            t_id = get_or_create_team(conn, r["Equipe"])
            c_id = get_or_create_car(conn, brand, model)
            
            # Insère le classement !
            save_result(conn, session_id, d_id, t_id, c_id, r["Pos"], r["Tours"], r["Temps"])
            print(f"🏎️  Inscrit : P{r['Pos']} - {first_name} {last_name} ({r['Temps']})")

        conn.close()
        print("\n🏁 Succès ! Tout le classement est en base de données.")
            
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    test_url = "https://www.touringcars.net/database/race.php?id=3209"
    extract_race_results(test_url)