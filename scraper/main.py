import requests
from bs4 import BeautifulSoup

# On importe nos outils de base de données !
from database import get_connection, get_or_create_driver, get_or_create_team, get_or_create_car

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def extract_race_results(url):
    print(f"Téléchargement des résultats de la course : {url}\n")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        rows = soup.find_all('div', class_='tb-row')
        
        results = []
        for row in rows:
            if 'header' in row.get('class', []): continue
                
            try:
                driver_div = row.find('div', class_='driver')
                driver_name = driver_div.find('a').text.strip() if driver_div and driver_div.find('a') else "Inconnu"
                
                entrant_div = row.find('div', class_='entrant')
                team = entrant_div.text.strip() if entrant_div else "Inconnue"
                
                car_div = row.find('div', class_='car')
                car = car_div.text.strip() if car_div else "Inconnue"
                
                results.append({"Pilote": driver_name, "Equipe": team, "Voiture": car})
            except AttributeError:
                continue

        print(f"✅ Extraction réussie : {len(results)} pilotes classés.")
        print("💾 Sauvegarde en base de données en cours...")
        
        # --- DÉBUT DE LA LOGIQUE DE SAUVEGARDE ---
        conn = get_connection()
        if not conn:
            print("❌ Annulation de la sauvegarde (Pas de DB).")
            return

        for r in results:
            # 1. On sépare le prénom et le nom (ex: "Gabriele TARQUINI" -> ["Gabriele", "TARQUINI"])
            name_parts = r["Pilote"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # 2. On sépare la marque et le modèle (ex: "Hyundai i30 N TCR" -> ["Hyundai", "i30 N TCR"])
            car_parts = r["Voiture"].split(" ", 1)
            brand = car_parts[0]
            model = car_parts[1] if len(car_parts) > 1 else ""

            # 3. On insère dans la BDD (ou on récupère l'ID si déjà existant)
            driver_id = get_or_create_driver(conn, first_name, last_name)
            team_id = get_or_create_team(conn, r["Equipe"])
            car_id = get_or_create_car(conn, brand, model)

            print(f"-> Sauvegardé : {first_name} {last_name} (ID: {driver_id}) | {brand} (ID: {car_id})")

        conn.close()
        print("\n🎉 Toutes les entités ont été synchronisées avec PostgreSQL !")
            
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    test_url = "https://www.touringcars.net/database/race.php?id=3209"
    extract_race_results(test_url)